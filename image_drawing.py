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

    def draw_aim(self, zoom_scale=1):
        height, width, _ = self.frame.shape
        center_x = width // 2
        center_y = height // 2
        rect_size = int(20 / zoom_scale)
        rect_thickness = 1 if zoom_scale > 3 else 2
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
        cv2.putText(self.frame, f"Cursor: x={cursor_x}, y={cursor_y}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255),
                    2)
        # cv2.putText(frame, f"KCF TRACKER", (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 255), 2)
        # cv2.putText(frame, f"CSRT TRACKER", (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 255), 2)
        cv2.putText(self.frame, f"MIL TRACKER", (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 255), 2)
        return self.frame
