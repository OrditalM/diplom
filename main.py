import threading
import queue
import time

import cv2

frames_qu = queue.Queue()

def show_process():
    while True:
        print("asw")
        frame = frames_qu.get()
        cv2.imshow("test", frame)
        time.sleep(0.025)
        if cv2.waitKey(1) and 0xFF == "q":
            break
    return

t = threading.Thread(target=show_process)
t.start()

video_file = "./test.mp4"
cap = cv2.VideoCapture(video_file)

while True:
    ret, frame = cap.read()
    frames_qu.put(frame)
    time.sleep(0.025)
    print("111")
