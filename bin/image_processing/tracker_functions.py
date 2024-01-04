import cv2
import datetime
import os
from bin.constants import CameraConstants


class Trackers:
    tracker_1 = cv2.TrackerCSRT.create()
    tracker_2 = cv2.TrackerKCF.create()
    tracker_3 = cv2.TrackerMIL.create()


def draw_lines_to_edges(frame, bbox):
    x, y, w, h = [int(e) for e in bbox]
    center = (x + w // 2, y + h // 2)

    height, width, _ = frame.shape

    cv2.line(frame, center, (0, center[1]), (0, 255, 0), 2)
    cv2.line(frame, center, (width, center[1]), (0, 255, 0), 2)
    cv2.line(frame, center, (center[0], 0), (0, 255, 0), 2)
    cv2.line(frame, center, (center[0], height), (0, 255, 0), 2)

    return frame


def tracking_process(frame, tracking, tracking_ok, bbox, object_lost):
    height, width, _ = frame.shape
    center_x = width // 2
    center_y = height // 2

    if tracking:
        Trackers.tracker_1.init(frame, bbox)
        print(Trackers.tracker_1.init(frame, bbox))
        print(bbox)
        tracking_ok = True
        tracking = False
    bbox1 = [0, 0, 0, 0]
    target_center = [center_x, center_y]

    if tracking_ok:
        ret1, bbox1 = Trackers.tracker_1.update(frame)
        if ret1:
            bbox1 = [int(e) for e in bbox1]
            cv2.rectangle(frame, (bbox1[0], bbox1[1]), (bbox1[0] + bbox1[2], bbox1[1] + bbox1[3]), (0, 255, 0), 2)
            frame = draw_lines_to_edges(frame, bbox1)
            target_center = (bbox1[0] + bbox1[2] // 2, bbox1[1] + bbox1[3] // 2)
        else:
            object_lost = True
            tracking_ok = False
    return frame, bbox1, tracking, object_lost, tracking_ok, target_center


def distance_calculator(frame, bbox1, real_object_width):
    if not bbox1 == [0,0,0,0]:
        camera = CameraConstants(os.getenv("MAIN_CAMERA"))
        pixels_x, pixels_y = camera.image_size
        pixels_per_cm = pixels_x / camera.matrix_x
        x, y, w, h = [int(e) for e in bbox1]
        object_size = ((w / 2) / pixels_per_cm) / 100
        if object_size != 0:
            distance = (camera.focal_length * (real_object_width + object_size)) / object_size
        else:
            distance = 0
    else:
        distance = 0
    cv2.putText(frame, f"{round(distance, 2)} M", (100, 300), cv2.FONT_HERSHEY_DUPLEX, 0.6, (0, 255, 0), 2)
    return frame
