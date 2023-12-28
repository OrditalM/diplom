import cv2
import datetime
from constants import CameraConstants


class Trackers:
    tracker_1 = cv2.TrackerCSRT.create()
    tracker_2 = cv2.TrackerKCF.create()
    tracker_3 = cv2.TrackerMIL.create()


def tracking_process(frame, tracking, tracking_ok, bbox, real_object_width, start_tracking_time, object_lost):
    if tracking:
        Trackers.tracker_1.init(frame, bbox)
        print(Trackers.tracker_1.init(frame, bbox))
        print(bbox)
        tracking_ok = True
        tracking = False

    if tracking_ok:
        ret1, bbox1 = Trackers.tracker_1.update(frame)
        if ret1:
            x, y, w, h = [int(e) for e in bbox1]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)
            distance_calculator(frame, bbox1, real_object_width)
        else:
            object_lost = True
            tracking_time = datetime.datetime.now() - start_tracking_time
            cv2.putText(frame, f"Object Lost at {datetime.datetime.now() - start_tracking_time} moment", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
            tracking_ok = False
    return frame, tracking, object_lost, tracking_ok


def distance_calculator(frame, bbox1, real_object_width):
    pixels_x, pixels_y = 1080, 1920  # cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    pixels_per_cm = pixels_x / CameraConstants.matrix_x
    x, y, w, h = [int(e) for e in bbox1]
    object_size = ((w / 2) / pixels_per_cm) / 100
    D = (CameraConstants.focal_length * (real_object_width + object_size)) / object_size
    cv2.putText(frame, f"{round(D, 2)} M", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 255), 2)
    return frame