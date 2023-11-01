import time
import datetime

import cv2

object_lost = False
video_file = "./test.mp4"
cap = cv2.VideoCapture(video_file)
fps = 0
#tracker_1 = cv2.TrackerCSRT.create()
#tracker_1 = cv2.TrackerKCF.create()
tracker_1 = cv2.TrackerMIL.create()
#tracker_1 = cv2.TrackerGOTURN.create()
#tracker_1 = cv2.TrackerDaSiamRPN.create()
cursor_x, cursor_y = -1, -1
tracking = False
bbox = None
desired_fps = 60

tracking_time = datetime.datetime.now()

frame_count = 0
start_time = time.time()
start_tracking_time = datetime.datetime.now()

cap.set(cv2.CAP_PROP_FPS, 20)

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

ok = False

while True:
    timer = cv2.getTickCount()
    ret, frame = cap.read()
    if not ret:
        break

    if tracking:

        tracker_1.init(frame, bbox)
      #  tracker_2.init(frame, bbox)
       # tracker_3.init(frame, bbox)
       # tracker_4.init(frame, bbox)
       # tracker_5.init(frame, bbox)
        print(tracker_1.init(frame, bbox))
        print(bbox)
        ok = True
        tracking = False

    if ok:
        ret1, bbox1 = tracker_1.update(frame)
      #  ret2, bbox2 = tracker_2.update(frame)
      #  ret3, bbox3 = tracker_3.update(frame)
       # ret4, bbox4 = tracker_4.update(frame)
      #  ret5, bbox5 = tracker_5.update(frame)
        if ret1:
            x, y, w, h = [int(e) for e in bbox1]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)

        else:
            object_lost = True
            tracking_time = datetime.datetime.now() - start_tracking_time
            cv2.putText(frame, f"Object Lost at {datetime.datetime.now() - start_tracking_time} moment", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
            ok = False

    height, width, _ = frame.shape

    center_x = width // 2
    center_y = height // 2

    rect_size = 200
    rect_thickness = 2

    top_left = (center_x - rect_size, center_y - rect_size)
    bottom_right = (center_x + rect_size, center_y + rect_size)

    cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), rect_thickness)
    cv2.line(frame, (center_x, center_y - rect_size - 10), (center_x, center_y - rect_size - 5), (0, 255, 0),
             rect_thickness)
    cv2.line(frame, (center_x, center_y + rect_size + 5), (center_x, center_y + rect_size + 10), (0, 255, 0),
             rect_thickness)
    cv2.line(frame, (center_x - rect_size - 10, center_y), (center_x - rect_size - 5, center_y), (0, 255, 0),
             rect_thickness)
    cv2.line(frame, (center_x + rect_size + 5, center_y), (center_x + rect_size + 10, center_y), (0, 255, 0),
             rect_thickness)

    cv2.putText(frame, f"Cursor: x={cursor_x}, y={cursor_y}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
    #cv2.putText(frame, f"KCF TRACKER", (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 255), 2)
    #cv2.putText(frame, f"CSRT TRACKER", (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 255), 2)
    cv2.putText(frame, f"MIL TRACKER", (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 255), 2)
    frame_count += 1
    if frame_count >= 10:  # Обчислення FPS кожні 10 кадрів
        end_time = time.time()
        elapsed_time = end_time - start_time
        fps = frame_count / elapsed_time
        start_time = end_time
        frame_count = 0
    cv2.putText(frame, f"FPS: {fps:.0f}", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
    if object_lost:
        cv2.putText(frame, f"Object Lost at {tracking_time} moment", (50, 350),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 255), 2)
    cv2.putText(frame, f"Object Lost at 0:00:26.263743 moment", (50, 350),
                cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 255), 2)
    cv2.imshow('Object Tracking', frame)

    key = cv2.waitKey(6) & 0xFF
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
