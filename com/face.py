
import cv2 as cv
import numpy as np
def face_detect_demo(image):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    face_detector = cv.CascadeClassifier("./haar/haarcascade_frontalface_default.xml")
    faces = face_detector.detectMultiScale(gray, 1.2, 6)
    for x, y, w, h in faces:
        cv.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)
    cv.imshow("result", image)

print("--------- Python OpenCV Tutorial ---------")

capture = cv.VideoCapture(0)
cv.namedWindow("result", cv.WINDOW_AUTOSIZE)
while(True):
    ret, frame = capture.read()
    frame = cv.flip(frame, 1)#左右翻转
    face_detect_demo(frame)
    c = cv.waitKey(10)
    if c == 27: # ESC
        break
cv.waitKey(0)
cv.destroyAllWindows()

