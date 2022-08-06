# bgr8转jpeg格式
import cv2
import json
import ipywidgets.widgets as widgets
import pyzbar.pyzbar as pyzbar
import matplotlib.pyplot as plt
from urllib.request import Request, urlopen
from CarHardwareControlModel import BuzzerControl

image_widget = widgets.Image(format='jpeg', width=320, height=240)
buzzerControl = BuzzerControl(buzzer=BuzzerControl.buzzer)


def bgr8_to_jpeg(value, quality=75):
    return bytes(cv2.imencode('.jpg', value)[1])


def getDataFromQRUrl(url):
    uid = url.split("/")[-1]
    url = "https://suishenmafront1.sh.gov.cn/smzy/yqfkewm/ssm/ewmcheck?uid={}".format(uid)

    headers = {}
    headers[b'Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8'
    request = Request(url, headers=headers)
    response = urlopen(request)

    jsonResponse = json.loads(response.read())
    return jsonResponse


# 定义解析二维码接口
def decodeDisplay(image):
    barcodes = pyzbar.decode(image)
    for barcode in barcodes:
        # 提取二维码的边界框的位置
        # 画出图像中条形码的边界框
        (x, y, w, h) = barcode.rect
        cv2.rectangle(image, (x, y), (x + w, y + h), (225, 225, 225), 2)

        # 提取二维码数据为字节对象，所以如果我们想在输出图像上
        # 画出来，就需要先将它转换成字符串
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type

        typeCode = "00"
        typeName = "Green"
        jsonResponse = getDataFromQRUrl(barcodeData)
        if jsonResponse["code"] == '0':
            typeCode = json.loads(jsonResponse['data'])["type"]
            print(typeCode)
            if typeCode == "00":
                typeName = "Green"
                print("绿色")
            elif typeCode == "01":
                typeName = "Yellow"
                buzzerControl.whistle(1)
                print("黄色")
            elif typeCode == "10":
                typeName = "Red"
                buzzerControl.whistle(2)
                print("红色")
        else:
            print(jsonResponse["message"])
        print(jsonResponse)

        # 绘出图像上条形码的数据和条形码类型
        text = "{} ({})".format(typeCode, typeName)
        cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (225, 225, 225), 2)
        # 向终端打印条形码数据和条形码类型
        print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))
    return image


def detect():
    plt.figure("QR Recognize")
    camera = cv2.VideoCapture(0)

    camera.set(3, 320)
    camera.set(4, 240)
    camera.set(5, 120)  # 设置帧率

    camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))
    camera.set(cv2.CAP_PROP_BRIGHTNESS, 40)  # 设置亮度 -64 - 64  0.0
    camera.set(cv2.CAP_PROP_CONTRAST, 50)  # 设置对比度 -64 - 64  2.0
    camera.set(cv2.CAP_PROP_EXPOSURE, 156)  # 设置曝光值 1.0 - 5000  156.0

    ret, frame = camera.read()
    image_widget.value = bgr8_to_jpeg(frame)
    while True:
        # 读取当前帧
        ret, frame = camera.read()
        # 转为灰度图像
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        im = decodeDisplay(gray)

        cv2.waitKey(5)
        image_widget.value = bgr8_to_jpeg(im)
        plt.imshow(im)
        plt.show()

        # 如果按键q则跳出本次循环
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()

detect()



