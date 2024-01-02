import cv2


class Colors:
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    black = (0, 0, 0)
    white = (255, 255, 255)
    yellow = (255, 255, 0)


class DrawFunctions:

    def __init__(self, frame):
        self.frame = frame

    def draw_aim(self):
        height, width, _ = self.frame.shape
        center_x = width // 2
        center_y = height // 2
        rect_size = 20
        rect_thickness = 2
        top_left = (center_x - rect_size, center_y - rect_size)
        bottom_right = (center_x + rect_size, center_y + rect_size)
        cv2.rectangle(self.frame, top_left, bottom_right, (0, 255, 0), rect_thickness)
        cv2.line(self.frame, (center_x, center_y - rect_size - 10), (center_x, center_y - rect_size - 100), Colors.green,
                 rect_thickness)
        cv2.line(self.frame, (center_x, center_y + rect_size + 10), (center_x, center_y + rect_size + 100), Colors.green,
                 rect_thickness)
        cv2.line(self.frame, (center_x - rect_size - 10, center_y), (center_x - rect_size - 100, center_y), Colors.green,
                 rect_thickness)
        cv2.line(self.frame, (center_x + rect_size + 10, center_y), (center_x + rect_size + 100, center_y), Colors.green,
                 rect_thickness)
        cv2.rectangle(self.frame, top_left, bottom_right, (0, 255, 0), rect_thickness)

        return self.frame

    def debug_info(self, cursor_x, cursor_y):
        cv2.putText(self.frame, f"Cursor: x={cursor_x}, y={cursor_y}", (50, 50), cv2.FONT_HERSHEY_DUPLEX, 0.75, (0, 0, 255),
                    2)
        # cv2.putText(frame, f"KCF TRACKER", (50, 250), cv2.FONT_HERSHEY_COMPLEX, 0.75, (0, 255, 255), 2)
        # cv2.putText(frame, f"CSRT TRACKER", (50, 250), cv2.FONT_HERSHEY_COMPLEX, 0.75, (0, 255, 255), 2)
        cv2.putText(self.frame, f"MIL TRACKER", (50, 250), cv2.FONT_HERSHEY_DUPLEX, 0.75, (0, 255, 255), 2)
        return self.frame

    def draw_control_keys(self):
        height, width, _ = self.frame.shape
        text = "Manual control keys:"
        x = 10
        y = height - 70
        cv2.putText(self.frame, text, (x, y), cv2.FONT_HERSHEY_DUPLEX, 0.75, (0, 255, 0), 2)
        text = "Turn ON ML: Y    Stop Tracking: C    Zoom IN: W    ZOOM Out: S    Select Tracking Object: F"
        x = 10
        y = height - 50
        cv2.putText(self.frame, text, (x, y), cv2.FONT_HERSHEY_DUPLEX, 0.6, (0, 255, 0), 2)
        return self.frame
