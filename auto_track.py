# -*- encoding: utf-8 -*-

import RPi.GPIO as GPIO
from com.convid.dog.CarHardwareControlModel import CarRunControl as crc


#红外避障接口
LSenso=26
RSenso=0

def init():
    #设置接触警告
    GPIO.setwarnings(False)
    #设置引脚模式为物理模式
    GPIO.setmode(GPIO.BOARD)
    #红外循迹传感器引脚初始化,设置为输入，接受红外信号
    GPIO.setup(LSenso,GPIO.IN)
    GPIO.setup(RSenso,GPIO.IN)

#红外循迹函数
def track():
    while True:
    	#接收两个红外传感器的信号
        LS=GPIO.input(LSenso)
        RS=GPIO.input(RSenso)
        #左右两个传感器都检测到黑色，小车在赛道上，前进
        if LS==True and RS==True:
            print("前进")
            crc.forward(16, 16, delaytime=0.1)
        #左边的传感器没检测到黑色，说明小车车身偏离赛道靠左，右转将小车车身向右调整
        elif LS==False and RS==True:
            print("右转")
            crc.right(18, 18, delaytime=0.1)
        #右边的传感器没检测到黑色，说明小车车身偏离赛道靠右，左转将小车车身向左调整
        elif LS==True and RS==False:
            print("左转")
            crc.left(18, 18, delaytime=0.1)
        #两个传感器都没有检测到黑色，说明小车完全偏离赛道，停止
        else:
            print("停止")
            crc.brake(0, 0, delaytime=0.1)
