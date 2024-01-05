import time

import cv2
import threading
import queue
from bin.image_processing.image_drawing import DrawFunctions
from bin.image_processing.tracker_functions import tracking_process, distance_calculator
from bin.image_processing.image_functions import zoom
from bin.config_parser import parse_config
from bin.flightcontroller_utils.SITL_drone_control import drone_control_thread
from bin.image_processing.neural_detection import detect_objects, load_model, load_labels, preprocess_image


parse_config()
object_lost = False
video_file = "./test.mp4"
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

img_buffer = queue.Queue()
ml_results = queue.Queue()
drone_control_queue = queue.Queue()

labels = load_labels()
model_path = 'Tensorflow/workspace/models/my_ssd_mobnet/export/saved_model/'
model = load_model(model_path)


def ml_detection_process():
    while True:
        time.sleep(0.025)
        if img_buffer.empty():
            continue
        else:
            ml_frame = img_buffer.get()[0]
            screen_size = img_buffer.get()[1]
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


def drone_thread():
    drone_control_thread(drone_control_queue)


def mouse_callback(event, x, y, flags, param):
    global cursor_x, cursor_y, tracking, bbox
    cv2.rectangle(frame, (x - int(object_image_size / 2), y - int(object_image_size / 2), object_image_size, object_image_size),
                  (0, 255, 0), 2)
    if event == cv2.EVENT_LBUTTONDOWN:
        cursor_x, cursor_y = x, y
        bbox = (x - int(object_image_size / 2), y - int(object_image_size / 2), object_image_size, object_image_size)
        tracking = True
        print("fefss")


cv2.namedWindow('Object Tracking')
cv2.setMouseCallback('Object Tracking', mouse_callback)

t_ml_detection = threading.Thread(target=ml_detection_process)
t_drone_control = threading.Thread(target=drone_thread)
t_ml_detection.start()
t_drone_control.start()

while True:
    timer = cv2.getTickCount()
    ret, frame = cap.read()
    screen_size = frame.shape
    original_frame = frame.copy()
    if not ret:
        break
    frame, bbox1, tracking, object_lost, tracking_ok, target_center = tracking_process(frame, tracking, tracking_ok, bbox, object_lost)
    key = cv2.waitKey(fps_limiter)
    zoom_point = target_center
    if key == ord('w'):
        zoom_factor = zoom_factor + 0.1 if zoom_factor < 5.0 else zoom_factor
    if key == ord('s'):
        zoom_factor = zoom_factor - 0.1 if zoom_factor > 1.0 else zoom_factor
    if key == ord('q'):
        object_image_size = object_image_size + 10 if object_image_size < 100 else object_image_size
    if key == ord('a'):
        object_image_size = object_image_size - 10 if object_image_size > 10 else object_image_size
    if key == ord('y'):
        ml_detection = True
    if key == ord('c'):
        tracking = False
        tracking_ok = False
    if key == ord('t'):
        ml_detection = False
    if key == ord('g'):
        start_flight = True
    if key == ord('h'):
        stop_flight = True


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

    frame = DrawFunctions(frame).draw_aim()
    frame = zoom(frame, zoom_factor, zoom_point)

    frame, target_distance = distance_calculator(frame, bbox1, real_object_width)
    if start_flight and tracking:
        drone_control_queue.put([target_center, screen_size, start_flight, stop_flight, target_distance])
    frame = DrawFunctions(frame).draw_control_keys()
    frame = DrawFunctions(frame).debug_info(cursor_x, cursor_y)

    cv2.imshow('Object Tracking', frame)

    #time.sleep(0.025)

    if key == ord(']'):
        break

cap.release()
cv2.destroyAllWindows()
