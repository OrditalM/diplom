import cv2

# Initialize the video capture object
video_file = "./test.mp4"
cap = cv2.VideoCapture(video_file)  # 0 for the default camera, or provide a video file path

tracker = cv2.TrackerGOTURN.create()
cursor_x, cursor_y = -1, -1  # Изначально координаты курсора отсутствуют
tracking = False
bbox = None

# Функция обработчика события мыши
def mouse_callback(event, x, y, flags, param):
    global cursor_x, cursor_y, tracking, bbox
    if event == cv2.EVENT_LBUTTONDOWN:
        cursor_x, cursor_y = x, y
        bbox = (x - 20, y - 20, 40, 40)  # Создание bounding box 100x100 вокруг клика
        tracking = True
        print("fefss")

cv2.namedWindow('Object Tracking')
cv2.setMouseCallback('Object Tracking', mouse_callback)

ok = False  # Инициализация переменной ok

while True:
    ret, frame = cap.read()
    if not ret:
        break

    if tracking:
        # Начать отслеживание объекта

        tracker.init(frame, bbox)
        print(tracker.init(frame, bbox))
        print(bbox)
        ok = True
        tracking = False

    if ok:
        ret, bbox = tracker.update(frame)
        if ret:
            x, y, w, h = [int(e) for e in bbox]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        else:
            cv2.putText(frame, "Object Lost", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

    height, width, _ = frame.shape

    # Определение центра кадра
    center_x = width // 2
    center_y = height // 2

    # Размер прицела и рамок
    rect_size = 200
    rect_thickness = 2

    # Определение координат углов прямоугольника для прицела
    top_left = (center_x - rect_size, center_y - rect_size)
    bottom_right = (center_x + rect_size, center_y + rect_size)

    # Рисование прицела и рамок
    cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), rect_thickness)
    cv2.line(frame, (center_x, center_y - rect_size - 10), (center_x, center_y - rect_size - 5), (0, 255, 0),
             rect_thickness)
    cv2.line(frame, (center_x, center_y + rect_size + 5), (center_x, center_y + rect_size + 10), (0, 255, 0),
             rect_thickness)
    cv2.line(frame, (center_x - rect_size - 10, center_y), (center_x - rect_size - 5, center_y), (0, 255, 0),
             rect_thickness)
    cv2.line(frame, (center_x + rect_size + 5, center_y), (center_x + rect_size + 10, center_y), (0, 255, 0),
             rect_thickness)

    # Вывод координат курсора
    cv2.putText(frame, f"Cursor: x={cursor_x}, y={cursor_y}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

    cv2.imshow('Object Tracking', frame)

    # Press 's' to select a new object to track or 'q' to exit
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

# Release the video capture and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
