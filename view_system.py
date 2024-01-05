# Import necessary libraries
import os
import time
import cv2
import threading
import queue
from bin.image_processing.image_drawing import DrawFunctions
from bin.image_processing.tracker_functions import tracking_process, distance_calculator
from bin.image_processing.image_functions import zoom
from bin.config_parser import parse_config
from bin.communications.nrf24_communication import main_comm_loop
from bin.flightcontroller_utils.SITL_drone_control import drone_control_thread
from bin.image_processing.neural_detection import detect_objects, load_model, load_labels, preprocess_image

# Parse configuration
parse_config()

# Initialize variables
object_lost = False
video_file = 0
cap = cv2.VideoCapture(video_file)
object_image_size = 40
cursor_x, cursor_y = -1, -1
tracking = False
bbox = None
ml_detection = False
start_flight = False
stop_flight = False
zoom_factor = 1.0
old_results = {}
real_object_width = 6
fps_limiter = 1
tracking_ok = False

# Initialize queues
img_buffer = queue.Queue()
ml_results = queue.Queue()
drone_control_queue = queue.Queue()
return_drone_info = queue.Queue()
input_comm_queue = queue.Queue()
output_comm_queue = queue.Queue()

# Load labels and model for neural detection
labels = load_labels()
model_path = 'Tensorflow/workspace/models/my_ssd_mobnet/export/saved_model/'
model = load_model(model_path)


# Function for ML detection process
def ml_detection_process():
    while True:
        time.sleep(0.025)
        if img_buffer.empty():
            continue
        else:
            ml_frame, screen_size = img_buffer.get()
            img = preprocess_image(ml_frame)
            res = detect_objects(model, img, 0.6)
            results_dict = {}

            for idx, result in enumerate(res):
                ymin, xmin, ymax, xmax = result['bounding_box']
                xmin = int(max(1, xmin * screen_size[1]))
                xmax = int(min(screen_size[1], xmax * screen_size[1]))
                ymin = int(max(1, ymin * screen_size[0]))
                ymax = int(min(screen_size[0], ymax * screen_size[0]))

                label = labels[result['class_id']]
                key = f'{label}_{idx}'
                results = [ymin, xmin, ymax, xmax]
                results_dict[key] = results
            ml_results.put(results_dict)


# Function for drone control thread
def drone_thread():
    drone_control_thread(drone_control_queue, return_drone_info)


# Function for communication thread
def communication_thread():
    main_comm_loop(input_comm_queue, output_comm_queue)


# Mouse callback function
def mouse_callback(event, x, y, flags, param):
    global cursor_x, cursor_y, tracking, bbox
    cv2.rectangle(frame, (
    x - int(object_image_size / 2), y - int(object_image_size / 2), object_image_size, object_image_size),
                  (0, 255, 0), 2)
    if event == cv2.EVENT_LBUTTONDOWN:
        cursor_x, cursor_y = x, y
        bbox = (x - int(object_image_size / 2), y - int(object_image_size / 2), object_image_size, object_image_size)
        tracking = True
        print("Start Tracking")


# Create a window for object tracking and set mouse callback
cv2.namedWindow('Object Tracking')
cv2.setMouseCallback('Object Tracking', mouse_callback)

# Start threads for ML detection, drone control, and communication
t_ml_detection = threading.Thread(target=ml_detection_process)
t_drone_control = threading.Thread(target=drone_thread)
t_communications = threading.Thread(target=communication_thread())
t_ml_detection.start()
t_drone_control.start()
# t_communications.start()

# Main loop
while True:
    timer = cv2.getTickCount()
    ret, frame = cap.read()
    screen_size = frame.shape
    original_frame = frame.copy()

    if not ret:
        break

    # Process tracking and key events
    frame, bbox1, tracking, object_lost, tracking_ok, target_center = tracking_process(frame, tracking, tracking_ok,
                                                                                       bbox, object_lost)

    if os.getenv("NRF_ON"):
        key_quit = cv2.waitKey(fps_limiter)
        input_comm_queue.put("Debug_Info")
        key = output_comm_queue.get()
    else:
        key = cv2.waitKey(fps_limiter)
        key_quit = cv2.waitKey(fps_limiter)

    zoom_point = target_center

    # Handle key events
    if key == ord('w'):
        zoom_factor = zoom_factor + 0.1 if zoom_factor < 5.0 else zoom_factor
    elif key == ord('s'):
        zoom_factor = zoom_factor - 0.1 if zoom_factor > 1.0 else zoom_factor
    elif key == ord('q'):
        object_image_size = object_image_size + 10 if object_image_size < 100 else object_image_size
    elif key == ord('a'):
        object_image_size = object_image_size - 10 if object_image_size > 10 else object_image_size
    elif key == ord('y'):
        ml_detection = True
    elif key == ord('c'):
        tracking = False
        tracking_ok = False
    elif key == ord('t'):
        ml_detection = False
    elif key == ord('g'):
        start_flight = True
    elif key == ord('h'):
        stop_flight = True

    # Process ML results and draw on frame
    if ml_results.empty():
        img_buffer.put([original_frame, screen_size])

    if ml_detection:
        if not ml_results.empty():
            results_dict = ml_results.get()
            old_results = results_dict.copy()
        for key, results in old_results.items():
            ymin, xmin, ymax, xmax = results
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 3)
            cv2.putText(frame, key, (xmin, min(ymax, screen_size[0] - 20)),
                        cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        old_results = old_results.copy()

    # Draw additional elements on the frame
    frame = DrawFunctions(frame).draw_aim()
    frame = zoom(frame, zoom_factor, zoom_point)
    print(start_flight, tracking_ok)
    frame, target_distance = distance_calculator(frame, bbox1, real_object_width)

    # Send control commands to the drone
    if start_flight and tracking_ok:
        drone_control_queue.put([target_center, screen_size, start_flight, stop_flight, target_distance])
        stop_flight = return_drone_info.get()

    frame = DrawFunctions(frame).draw_control_keys()
    frame = DrawFunctions(frame).debug_info(cursor_x, cursor_y)

    # Display the frame
    cv2.imshow('Object Tracking', frame)

    if key_quit == ord(']'):
        break

# Release video capture and close windows
cap.release()
cv2.destroyAllWindows()
