import time
import datetime

import cv2

from image_drawing import DrawFunctions
from constants import CameraConstants
from tracker_funct import tracking_process
from mouse_functions import zoom

object_lost = False
video_file = "./test_4.mp4"
cap = cv2.VideoCapture(video_file)
fps = 0

cursor_x, cursor_y = -1, -1
tracking = False
bbox = None
desired_fps = 60

zoom_factor = 1.0

real_object_width = 3

tracking_time = datetime.datetime.now()

frame_count = 0
start_time = time.time()
start_tracking_time = datetime.datetime.now()
pixels_x, pixels_y = 1080, 1920 # cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

cap.set(cv2.CAP_PROP_FPS, 20)

tracking_ok = False


def mouse_callback(event, x, y, flags, param):
    global cursor_x, cursor_y, tracking, bbox
    cv2.rectangle(frame, (x - 20, y - 20), (x + 40, y + 40), (0, 255, 0), 2)
    if event == cv2.EVENT_LBUTTONDOWN:
        cursor_x, cursor_y = x, y
        bbox = (x - 20, y - 20, 40, 40)
        tracking = True
        print("fefss")


cv2.namedWindow('Object Tracking')

cv2.setMouseCallback('Object Tracking', mouse_callback)

while True:
    pixels_per_cm = pixels_x / CameraConstants.matrix_x
    timer = cv2.getTickCount()
    ret, frame = cap.read()
    if not ret:
        break

    frame, tracking, object_lost, tracking_ok, target_center = tracking_process(frame, tracking, tracking_ok, bbox, real_object_width,
                                                                 start_tracking_time, object_lost)

    frame = DrawFunctions(frame).draw_aim(zoom_factor)

    frame = DrawFunctions(frame).debug_info(cursor_x, cursor_y)

    frame_count += 1
    if frame_count >= 10:
        end_time = time.time()
        elapsed_time = end_time - start_time
        fps = frame_count / elapsed_time
        start_time = end_time
        frame_count = 0
    cv2.putText(frame, f"FPS: {fps:.0f}", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
    if object_lost:
        cv2.putText(frame, f"Object Lost at {tracking_time} moment", (50, 350),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 255), 2)

    key = cv2.waitKey(30)
    zoom_point = target_center
    if key == ord('w'):
        zoom_factor = zoom_factor + 0.1 if zoom_factor < 5.0 else zoom_factor

    if key == ord('s'):
        zoom_factor = zoom_factor - 0.1 if zoom_factor > 1.0 else zoom_factor

    frame = zoom(frame, zoom_factor, zoom_point)

    cv2.imshow('Object Tracking', frame)

    if key == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
