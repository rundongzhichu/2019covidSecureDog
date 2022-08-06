import cv2
import ipywidgets.widgets as widgets

from com.convid.dog.CarHardwareControlModel import CarRunControl, ServoControl

crc = CarRunControl(20, 21, 16, 19, 26, 13, 100, 100)
lrServo = ServoControl(ServoControl.CameraLeftRightServoPin)
udServo = ServoControl(ServoControl.CameraUpDownServoPinB)

# 设置图像大小
width, height = 160, 120
image_widget = widgets.Image(format='jpeg', width=width, height=height)

def bgr8_to_jpeg(value, quality=75):
    return bytes(cv2.imencode('.jpg', value)[1])

def track_to_people(x, y):
    global second
    # stop
    if x == 0 and y == 0:
        crc.brake()
    # go ahead
    elif width / 4 < x and x < (width - width / 4) and height / 4 < y and y < (height - height / 4):
        crc.forward(100, 100)
    # left
    elif x < width / 4:
        crc.left(0, 50)
    # Right
    elif x > (width - width / 4):
        crc.right(50, 0)
    elif y < height / 4:
        crc.back(100, 100)
    elif y > (height - height / 4):
        crc.forward(100, 100)


def face_detect(image):
    try:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        face_detector = cv2.CascadeClassifier("./haar/haarcascade_frontalface_default.xml")
        # face_detector = cv2.CascadeClassifier("./haar/haarcascade_upperbody.xml")
        # face_detector = cv2.CascadeClassifier("./haar/haarcascade_profileface.xml")
        # face_detector = cv2.CascadeClassifier("./haar/haarcascade_fullbody.xml")
        # face_detector = cv2.CascadeClassifier("./haar/haarcascade_eye.xml")
        # face_detector = cv2.CascadeClassifier("./haar/haarcascade_eye_tree_eyeglasses.xml")
        faces = face_detector.detectMultiScale(gray, 1.1, 3)
        for x, y, w, h in faces:
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)
        return image, faces[0]
    except Exception as e:
        print("no face detected!")

def run_toward_people():
    camera = cv2.VideoCapture(0)
    camera.set(3, width)
    camera.set(4, height)

    while True:
        # 设置摄像头云台舵机的初始位置
        lrServo.change_duty_cycle_by_angle(90)
        udServo.change_duty_cycle_by_angle(45)

        ret, frame = camera.read()
        frame = cv2.flip(frame, 1)#左右翻转
        frame, (x, y, w, h) = face_detect(frame)
        image_widget.value = bgr8_to_jpeg(frame)
        track_to_people(x, y)

        c = cv2.waitKey(10)
        if c == 27:  # ESC
            break
    camera.release()
    cv2.waitKey(0)
    cv2.destroyAllWindows()

run_toward_people()
