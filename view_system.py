import time
import datetime
import cv2
import threading
import queue
from bin.image_processing.image_drawing import DrawFunctions
from bin.image_processing.tracker_functions import tracking_process, distance_calculator
from bin.image_processing.image_functions import zoom
from bin.config_parser import parse_config
from bin.image_processing.neural_detection import detect_objects, load_model, load_labels, preprocess_image


parse_config()
object_lost = False
video_file = "./test.mp4"
cap = cv2.VideoCapture(video_file)
fps = 0

object_image_size = 40

cursor_x, cursor_y = -1, -1
tracking = False
bbox = None
desired_fps = 60
ml_detection = False
global ml_detection
zoom_factor = 1.0

real_object_width = 6

tracking_time = datetime.datetime.now()

frame_count = 0
start_time = time.time()
start_tracking_time = datetime.datetime.now()

cap.set(cv2.CAP_PROP_FPS, 20)

tracking_ok = False

image_buffer = queue.Queue()
message_buffer = queue.Queue()
target_coord_buffer = queue.Queue()
ml_results_buffer = queue.Queue()
final_image_buffer = queue.Queue()

labels = load_labels()
model_path = 'Tensorflow\workspace\models\my_ssd_mobnet\export\saved_model\\'
model = load_model(model_path)


def ml_detection_process():
    ml_frame = image_buffer.get()
    screen_size = ml_frame.shape
    img = preprocess_image(ml_frame)
    res = detect_objects(model, img, 0.6)
    for result in res:
        ymin, xmin, ymax, xmax = result['bounding_box']
        xmin = int(max(1, xmin * screen_size[1]))
        xmax = int(min(screen_size[1], xmax * screen_size[1]))
        ymin = int(max(1, ymin * screen_size[0]))
        ymax = int(min(screen_size[0], ymax * screen_size[0]))
        cv2.rectangle(ml_frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 3)
        cv2.putText(ml_frame, labels[result['class_id']], (xmin, min(ymax, screen_size[0] - 20)),
                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        ml_results_buffer.put(ml_frame)


def im_show_frame():
    queue_frame = final_image_buffer.get()
    cv2.imshow('Object Tracking', queue_frame)


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


while True:
    timer = cv2.getTickCount()
    ret, frame = cap.read()
    if not ret:
        break
    if ml_detection:
        screen_size = frame.shape
        img = preprocess_image(frame)
        res = detect_objects(model, img, 0.6)
        for result in res:
            ymin, xmin, ymax, xmax = result['bounding_box']
            xmin = int(max(1, xmin * screen_size[1]))
            xmax = int(min(screen_size[1], xmax * screen_size[1]))
            ymin = int(max(1, ymin * screen_size[0]))
            ymax = int(min(screen_size[0], ymax * screen_size[0]))
            results = [ymin, xmin, ymax, xmax]

            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 3)
            cv2.putText(frame, labels[result['class_id']], (xmin, min(ymax, screen_size[0] - 20)),
                        cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

    frame, bbox1, tracking, object_lost, tracking_ok, target_center = tracking_process(frame, tracking, tracking_ok,
                                                                                           bbox,
                                                                                           start_tracking_time,
                                                                                           object_lost)
    frame_count += 1
    if frame_count >= 10:
        end_time = time.time()
        elapsed_time = end_time - start_time
        fps = frame_count / elapsed_time
        start_time = end_time
        frame_count = 0
    cv2.putText(frame, f"FPS: {fps:.0f}", (50, 150), cv2.FONT_HERSHEY_COMPLEX, 0.75, (0, 0, 255), 2)
    if object_lost:
        cv2.putText(frame, f"Object Lost at {tracking_time} moment", (50, 350),
                    cv2.FONT_HERSHEY_COMPLEX, 0.75, (0, 255, 255), 2)

    fps_limiter = 20 if not ml_detection else 1

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

    frame = DrawFunctions(frame).draw_aim()

    frame = zoom(frame, zoom_factor, zoom_point)

    frame = distance_calculator(frame, bbox1, real_object_width)
    frame = DrawFunctions(frame).draw_control_keys()
    frame = DrawFunctions(frame).debug_info(cursor_x, cursor_y)

    cv2.imshow('Object Tracking', frame)

    if key == ord(']'):
        break
cap.release()
cv2.destroyAllWindows()
