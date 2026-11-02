import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import os
import traceback

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dataset_dir = os.path.join(BASE_DIR, "AtoZ_3.1")

capture = cv2.VideoCapture(0)
hd = HandDetector(maxHands=1)
hd2 = HandDetector(maxHands=1)

c_dir = 'A'
target_dir = os.path.join(dataset_dir, c_dir)
os.makedirs(target_dir, exist_ok=True)
count = len(os.listdir(target_dir))

offset = 15
step = 1
flag = False
suv = 0

while True:
    try:
        ret, frame = capture.read()
        if not ret or frame is None:
            continue
        frame = cv2.flip(frame, 1)
        hands, _ = hd.findHands(frame, draw=False, flipType=True)
        white = np.ones((400, 400, 3), dtype=np.uint8) * 255

        if hands:
            hand = hands[0]
            x, y, w, h = hand['bbox']
            h_f, w_f = frame.shape[:2]
            y1 = max(0, y - offset)
            y2 = min(h_f, y + h + offset)
            x1 = max(0, x - offset)
            x2 = min(w_f, x + w + offset)

            if y2 > y1 and x2 > x1:
                image = frame[y1:y2, x1:x2]
                handz, imz = hd2.findHands(image, draw=True, flipType=True)
                if handz:
                    hand = handz[0]
                    pts = hand['lmList']
                    os_x = ((400 - w) // 2) - 15
                    os_y = ((400 - h) // 2) - 15
                    for t in range(0, 4, 1):
                        cv2.line(white, (pts[t][0] + os_x, pts[t][1] + os_y), (pts[t + 1][0] + os_x, pts[t + 1][1] + os_y), (0, 255, 0), 3)
                    for t in range(5, 8, 1):
                        cv2.line(white, (pts[t][0] + os_x, pts[t][1] + os_y), (pts[t + 1][0] + os_x, pts[t + 1][1] + os_y), (0, 255, 0), 3)
                    for t in range(9, 12, 1):
                        cv2.line(white, (pts[t][0] + os_x, pts[t][1] + os_y), (pts[t + 1][0] + os_x, pts[t + 1][1] + os_y), (0, 255, 0), 3)
                    for t in range(13, 16, 1):
                        cv2.line(white, (pts[t][0] + os_x, pts[t][1] + os_y), (pts[t + 1][0] + os_x, pts[t + 1][1] + os_y), (0, 255, 0), 3)
                    for t in range(17, 20, 1):
                        cv2.line(white, (pts[t][0] + os_x, pts[t][1] + os_y), (pts[t + 1][0] + os_x, pts[t + 1][1] + os_y), (0, 255, 0), 3)
                    cv2.line(white, (pts[5][0] + os_x, pts[5][1] + os_y), (pts[9][0] + os_x, pts[9][1] + os_y), (0, 255, 0), 3)
                    cv2.line(white, (pts[9][0] + os_x, pts[9][1] + os_y), (pts[13][0] + os_x, pts[13][1] + os_y), (0, 255, 0), 3)
                    cv2.line(white, (pts[13][0] + os_x, pts[13][1] + os_y), (pts[17][0] + os_x, pts[17][1] + os_y), (0, 255, 0), 3)
                    cv2.line(white, (pts[0][0] + os_x, pts[0][1] + os_y), (pts[5][0] + os_x, pts[5][1] + os_y), (0, 255, 0), 3)
                    cv2.line(white, (pts[0][0] + os_x, pts[0][1] + os_y), (pts[17][0] + os_x, pts[17][1] + os_y), (0, 255, 0), 3)

                    for i in range(21):
                        cv2.circle(white, (pts[i][0] + os_x, pts[i][1] + os_y), 2, (0, 0, 255), 1)

                    cv2.imshow("skeleton", white)

        frame = cv2.putText(frame, f"Letter: {c_dir} Count: {count} Rec: {flag}", (30, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.imshow("frame", frame)
        interrupt = cv2.waitKey(1)
        if interrupt & 0xFF == 27:
            # esc key
            break

        if interrupt & 0xFF == ord('n'):
            c_dir = chr(ord(c_dir) + 1)
            if ord(c_dir) > ord('Z'):
                c_dir = 'A'
            flag = False
            target_dir = os.path.join(dataset_dir, c_dir)
            os.makedirs(target_dir, exist_ok=True)
            count = len(os.listdir(target_dir))

        if interrupt & 0xFF == ord('a'):
            if flag:
                flag = False
            else:
                suv = 0
                flag = True

        if flag:
            if suv >= 180:
                flag = False
            if step % 3 == 0:
                target_dir = os.path.join(dataset_dir, c_dir)
                os.makedirs(target_dir, exist_ok=True)
                cv2.imwrite(os.path.join(target_dir, f"{count}.jpg"), white)
                count += 1
                suv += 1
            step += 1

    except Exception:
        print("==", traceback.format_exc())

capture.release()
cv2.destroyAllWindows()
