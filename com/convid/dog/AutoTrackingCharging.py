# -*- encoding: utf-8 -*-
import time

from com.convid.dog.CarHardwareControlModel import TrackingSensorControl, CarRunControl

tsc = TrackingSensorControl(3, 5, 4, 18)
crc = CarRunControl(20, 21, 16, 19, 26, 13)

#红外循迹函数
def track():
    while True:
        if tsc.is_right_actute_angle_or_right_angle():
            crc.spin_right(35, 30)
            time.sleep(0.1)
        elif tsc.is_left_actute_angle_or_right_angle():
            crc.spin_left(30, 35)
            time.sleep(0.1)
        elif tsc.is_far_left_dectected():
            crc.spin_left(30, 30)
        elif tsc.is_far_right_dectected():
            crc.spin_right(30, 30)
        elif tsc.is_small_left_bend():
            crc.left(0, 35)
        elif tsc.is_small_right_bend():
            crc.right(35, 0)
        elif tsc.is_straight():
            crc.forward(35, 35)
        else:
            crc.brake(0, 0)


