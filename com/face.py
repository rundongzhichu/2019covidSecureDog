
import cv2
import numpy as np

def face_detect_demo(image):
    gray = cv2.cvtColor(image, cv.COLOR_BGR2GRAY)
    face_detector = cv2.CascadeClassifier("./haar/haarcascade_frontalface_default.xml")
    # face_detector = cv2.CascadeClassifier("./haar/haarcascade_upperbody.xml")
    # face_detector = cv2.CascadeClassifier("./haar/haarcascade_profileface.xml")
    # face_detector = cv2.CascadeClassifier("./haar/haarcascade_fullbody.xml")
    # face_detector = cv2.CascadeClassifier("./haar/haarcascade_eye.xml")
    # face_detector = cv2.CascadeClassifier("./haar/haarcascade_eye_tree_eyeglasses.xml")
    faces = face_detector.detectMultiScale(gray, 1.1, 3)
    for x, y, w, h in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)
    cv2.imshow("result", image)

print("--------- Python OpenCV Tutorial ---------")

capture = cv2.VideoCapture(0)
cv2.namedWindow("result", cv2.WINDOW_AUTOSIZE)
while(True):
    ret, frame = capture.read()
    frame = cv2.flip(frame, 1)#左右翻转
    face_detect_demo(frame)
    c = cv2.waitKey(10)
    if c == 27: # ESC
        break
cv2.waitKey(0)
cv2.destroyAllWindows()

# Object Tracking
import RPi.GPIO as GPIO
import time
import Adafruit_PCA9685
import numpy as np
import cv2

second = 0

width, height = 160, 120
camera = cv2.VideoCapture(0)
camera.set(3, width)
camera.set(4, height)

l_motor = 18
left_front = 22
left_back = 27

r_motor = 23
right_front = 25
right_back = 24


def Motor_Init():
    global L_Motor, R_Motor
    L_Motor = GPIO.PWM(l_motor, 100)
    R_Motor = GPIO.PWM(r_motor, 100)
    L_Motor.start(0)
    R_Motor.start(0)


def Direction_Init():
    GPIO.setup(left_back, GPIO.OUT)
    GPIO.setup(left_front, GPIO.OUT)
    GPIO.setup(l_motor, GPIO.OUT)

    GPIO.setup(right_front, GPIO.OUT)
    GPIO.setup(right_back, GPIO.OUT)
    GPIO.setup(r_motor, GPIO.OUT)


def Servo_Init():
    global pwm_servo
    pwm_servo = Adafruit_PCA9685.PCA9685()


def Init():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    Direction_Init()
    Servo_Init()
    Motor_Init()


def Front(speed):
    L_Motor.ChangeDutyCycle(speed)
    GPIO.output(left_front, 1)  # left_front
    GPIO.output(left_back, 0)  # left_back

    R_Motor.ChangeDutyCycle(speed)
    GPIO.output(right_front, 1)  # right_front
    GPIO.output(right_back, 0)  # right_back


def Back(speed):
    L_Motor.ChangeDutyCycle(speed)
    GPIO.output(left_front, 0)  # left_front
    GPIO.output(left_back, 1)  # left_back

    R_Motor.ChangeDutyCycle(speed)
    GPIO.output(right_front, 0)  # right_front
    GPIO.output(right_back, 1)  # right_back


def Left(speed):
    L_Motor.ChangeDutyCycle(speed)
    GPIO.output(left_front, 0)  # left_front
    GPIO.output(left_back, 1)  # left_back

    R_Motor.ChangeDutyCycle(speed)
    GPIO.output(right_front, 1)  # right_front
    GPIO.output(right_back, 0)  # right_back


def Right(speed):
    L_Motor.ChangeDutyCycle(speed)
    GPIO.output(left_front, 1)  # left_front
    GPIO.output(left_back, 0)  # left_back

    R_Motor.ChangeDutyCycle(speed)
    GPIO.output(right_front, 0)  # right_front
    GPIO.output(right_back, 1)  # right_back


def Stop():
    L_Motor.ChangeDutyCycle(0)
    GPIO.output(left_front, 0)  # left_front
    GPIO.output(left_back, 0)  # left_back

    R_Motor.ChangeDutyCycle(0)
    GPIO.output(right_front, 0)  # right_front
    GPIO.output(right_back, 0)  # right_back


def set_servo_angle(channel, angle):
    angle = 4096 * ((angle * 11) + 500) / 20000
    pwm_servo.set_pwm_freq(50)  # frequency==50Hz (servo)
    pwm_servo.set_pwm(channel, 0, int(angle))


def Image_Processing():
    # Capture the frames
    ret, frame = camera.read()
    # Crop the image
    image = frame
    cv2.imshow('frame', frame)
    # to gray
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('gray', gray)
    # Gausi blur
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    # brighten
    blur = cv2.convertScaleAbs(blur, None, 1.5, 30)
    # to binary
    ret, binary = cv2.threshold(blur, 150, 255, cv2.THRESH_BINARY_INV)
    cv2.imshow('binary', binary)
    # Close
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (17, 17))
    close = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    cv2.imshow('close', close)
    # get contours
    binary_c, contours, hierarchy = cv2.findContours(close, 1, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(image, contours, -1, (255, 0, 255), 2)
    cv2.imshow('image', image)
    return frame, contours


def Get_Coord(img, contours):
    image = img.copy()
    try:
        contour = max(contours, key=cv2.contourArea)
        cv2.drawContours(image, contour, -1, (255, 0, 255), 2)
        cv2.imshow('new_frame', image)
        # get coord
        M = cv2.moments(contour)
        x = int(M['m10'] / M['m00'])
        y = int(M['m01'] / M['m00'])
        print(x, y)
        return x, y

    except:
        print
        'no objects'
        return 0, 0


def Move(x, y):
    global second
    # stop
    if x == 0 and y == 0:
        Stop()
    # go ahead
    elif width / 4 < x and x < (width - width / 4):
        Front(70)
    # left
    elif x < width / 4:
        Left(50)
    # Right
    elif x > (width - width / 4):
        Right(50)


if __name__ == '__main__':
    Init()

    set_servo_angle(4, 110)  # top servo     lengthwise
    # 0:back    180:front
    set_servo_angle(5, 90)  # bottom servo  crosswise
    # 0:left    180:right

    while 1:
        # 1 Image Process
        img, contours = Image_Processing()

        # 2 get coordinates
        x, y = Get_Coord(img, contours)

        # 3 Move
        Move(x, y)

        # must include this codes(otherwise you can't open camera successfully)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            Stop()
            GPIO.cleanup()
            break

    # Front(50)
    # Back(50)
    # $Left(50)
    # Right(50)
    # time.sleep(1)
    # Stop()


