import cv2


def mouse_callback(frame, event, x, y, flags, param):
    cv2.rectangle(frame, (x - 20, y - 20), (x + 40, y + 40), (0, 255, 0), 2)
    if event == cv2.EVENT_LBUTTONDOWN:
        cursor_x, cursor_y = x, y
        bbox = (x - 20, y - 20, 40, 40)
        tracking = True
        print("fefss")
        return cursor_x, cursor_y, tracking, bbox
