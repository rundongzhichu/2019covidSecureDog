# -*- coding:UTF-8 -*-
import RPi.GPIO as GPIO
import time

class ColorLEDControl:

    #RGB三色灯引脚定义
    LED_R = 22
    LED_G = 27
    LED_B = 24

    def __init__(self,LED_R,LED_G,LED_B,mode="BCM"):
        # 忽略警告信息
        GPIO.setwarnings(False)
        self.set_mode(mode)
        self.LED_R = LED_R
        self.LED_B = LED_B
        self.LED_G = LED_G
        self.pin_state_init()

    def set_mode(self,mode="BCM"):
        if mode == "BCM":
            #设置RGB三色灯为BCM编码方式
            GPIO.setmode(GPIO.BCM)

    def pin_state_init(self,):
        GPIO.setup(self.LED_R,GPIO.OUT)
        GPIO.setup(self.LED_G, GPIO.OUT)
        GPIO.setup(self.LED_B, GPIO.OUT)

    def set_pin_model(self, pin, model=GPIO.OUT):
        #RGB三色灯设置为输出模式
        GPIO.setup(pin, model)

    def turn_on_RED(self,):
        GPIO.output(self.LED_R, GPIO.HIGH)

    def turn_on_GREEN(self,):
        GPIO.output(self.LED_G, GPIO.HIGH)

    def turn_on_BLUE(self,):
        GPIO.output(self.LED_B, GPIO.HIGH)

    def turn_off_RED(self, ):
        GPIO.output(self.LED_R, GPIO.LOW)

    def turn_off_GREEN(self, ):
        GPIO.output(self.LED_G, GPIO.LOW)

    def turn_off_BLUE(self, ):
        GPIO.output(self.LED_B, GPIO.LOW)

    def clean_pin_state(self,):
        GPIO.cleanup()

class CarRunControl:

    # 小车电机引脚定义
    LEFT_IN1 = 20
    LEFT_IN2 = 21
    LEFT_ENA = 16
    RIGHT_IN1 = 19
    RIGHT_IN2 = 26
    RIGHT_ENB = 13

    def __init__(self,LEFT_IN1,LEFT_IN2,LEFT_ENA,RIGHT_IN1,RIGHT_IN2,RIGHT_ENB,left_ena_pwm=2000,right_enb_pwm=2000,mode="BCM"):
        # 忽略警告信息
        GPIO.setwarnings(False)
        self.set_mode(mode)
        self.LEFT_IN1=LEFT_IN1
        self.LEFT_IN2=LEFT_IN2
        self.LEFT_ENA=LEFT_ENA

        self.RIGHT_IN1 = RIGHT_IN1
        self.RIGHT_IN2 = RIGHT_IN2
        self.RIGHT_ENB = RIGHT_ENB
        self.motor_init(left_ena_pwm,right_enb_pwm)

    def set_mode(self, mode="BCM"):
        if mode == "BCM":
            #设置RGB三色灯为BCM编码方式
            GPIO.setmode(GPIO.BCM)

    # 电机引脚初始化操作
    def motor_init(self,left_ena_pwm=2000,right_enb_pwm=2000):
        GPIO.setup(self.LEFT_ENA, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(self.LEFT_IN1, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.LEFT_IN2, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.RIGHT_ENB, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(self.RIGHT_IN1, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.RIGHT_IN2, GPIO.OUT, initial=GPIO.LOW)
        # 设置pwm引脚和频率为2000hz
        self.pwm_LFT_ENA = GPIO.PWM(self.LEFT_ENA, left_ena_pwm)
        self.pwm_RIGHT_ENB = GPIO.PWM(self.RIGHT_ENB, right_enb_pwm)
        self.pwm_LFT_ENA.start(0)
        self.pwm_RIGHT_ENB.start(0)

    def set_pin_model(self, pin, model=GPIO.OUT):
        # 设置pin的状态
        GPIO.setup(pin, model)

    def set_pwm(self,left_ena_pwm=2000,right_enb_pwm=2000):
        if self.pwm_LFT_ENA is not None :
            self.pwm_LFT_ENA.stop()

        if self.pwm_RIGHT_ENB is not None :
            self.pwm_RIGHT_ENB.stop()

        # 设置pwm引脚和频率为?hz,默认2000hz
        self.pwm_LFT_ENA = GPIO.PWM(self.LEFT_ENA, left_ena_pwm)
        self.pwm_RIGHT_ENB = GPIO.PWM(self.RIGHT_ENB, right_enb_pwm)
        self.pwm_LFT_ENA.start(0)
        self.pwm_RIGHT_ENB.start(0)

    def set_left_ena_pwm(self, pwm=2000):
        # 设置pwm引脚和频率为?hz,默认2000hz
        self.pwm_LFT_ENA = GPIO.PWM(self.LEFT_ENA, pwm)
        self.pwm_LFT_ENA.start(0)

    def set_right_enb_pwm(self, pwm=2000):
        # 设置pwm引脚和频率为?hz,默认2000hz
        self.pwm_RIGHT_ENB = GPIO.PWM(self.RIGHT_ENB, pwm)
        self.pwm_RIGHT_ENB.start(0)

    # 小车前进
    def forward(self,leftspeed, rightspeed,delaytime=0):
        GPIO.output(self.LEFT_IN1, GPIO.HIGH)
        GPIO.output(self.LEFT_IN2, GPIO.LOW)
        GPIO.output(self.RIGHT_IN1, GPIO.HIGH)
        GPIO.output(self.RIGHT_IN2, GPIO.LOW)
        self.pwm_LFT_ENA.ChangeDutyCycle(leftspeed)
        self.pwm_RIGHT_ENB.ChangeDutyCycle(rightspeed)
        time.sleep(delaytime)

    # 小车后退
    def back(self,leftspeed, rightspeed,delaytime=0):
        GPIO.output(self.LEFT_IN1, GPIO.LOW)
        GPIO.output(self.LEFT_IN2, GPIO.HIGH)
        GPIO.output(self.RIGHT_IN1, GPIO.LOW)
        GPIO.output(self.RIGHT_IN2, GPIO.HIGH)
        self.pwm_LFT_ENA.ChangeDutyCycle(leftspeed)
        self.pwm_RIGHT_ENB.ChangeDutyCycle(rightspeed)
        time.sleep(delaytime)

    # 小车左转
    def left(self,leftspeed, rightspeed,delaytime=0):
        GPIO.output(self.LEFT_IN1, GPIO.LOW)
        GPIO.output(self.LEFT_IN2, GPIO.LOW)
        GPIO.output(self.RIGHT_IN1, GPIO.HIGH)
        GPIO.output(self.RIGHT_IN2, GPIO.LOW)
        self.pwm_LFT_ENA.ChangeDutyCycle(leftspeed)
        self.pwm_RIGHT_ENB.ChangeDutyCycle(rightspeed)
        time.sleep(delaytime)

    # 小车右转
    def right(self,leftspeed, rightspeed,delaytime=0):
        GPIO.output(self.LEFT_IN1, GPIO.HIGH)
        GPIO.output(self.LEFT_IN2, GPIO.LOW)
        GPIO.output(self.RIGHT_IN1, GPIO.LOW)
        GPIO.output(self.RIGHT_IN2, GPIO.LOW)
        self.pwm_LFT_ENA.ChangeDutyCycle(leftspeed)
        self.pwm_RIGHT_ENB.ChangeDutyCycle(rightspeed)
        time.sleep(delaytime)

    # 小车原地左转
    def spin_left(self,leftspeed, rightspeed,delaytime=0):
        GPIO.output(self.LEFT_IN1, GPIO.LOW)
        GPIO.output(self.LEFT_IN2, GPIO.HIGH)
        GPIO.output(self.RIGHT_IN1, GPIO.HIGH)
        GPIO.output(self.RIGHT_IN2, GPIO.LOW)
        self.pwm_LFT_ENA.ChangeDutyCycle(leftspeed)
        self.pwm_RIGHT_ENB.ChangeDutyCycle(rightspeed)
        time.sleep(delaytime)

    # 小车原地右转
    def spin_right(self,leftspeed, rightspeed,delaytime=0):
        GPIO.output(self.LEFT_IN1, GPIO.HIGH)
        GPIO.output(self.LEFT_IN2, GPIO.LOW)
        GPIO.output(self.RIGHT_IN1, GPIO.LOW)
        GPIO.output(self.RIGHT_IN2, GPIO.HIGH)
        self.pwm_LFT_ENA.ChangeDutyCycle(leftspeed)
        self.pwm_RIGHT_ENB.ChangeDutyCycle(rightspeed)
        time.sleep(delaytime)

    # 小车停止
    def brake(self,leftspeed=0, rightspeed=0,delaytime=0):
        GPIO.output(self.LEFT_IN1, GPIO.LOW)
        GPIO.output(self.LEFT_IN2, GPIO.LOW)
        GPIO.output(self.RIGHT_IN1, GPIO.LOW)
        GPIO.output(self.RIGHT_IN2, GPIO.LOW)
        self.pwm_LFT_ENA.ChangeDutyCycle(leftspeed)
        self.pwm_RIGHT_ENB.ChangeDutyCycle(rightspeed)
        time.sleep(delaytime)

    def clean_pin_state(self,):
        self.pwm_LFT_ENA.stop()
        self.pwm_RIGHT_ENB.stop()
        GPIO.cleanup()


class ServoControl:

    # 舵机引脚定义
    UltrasonicServoPin = 23
    CameraLeftRightServoPin = 10  # S4 换一个插口解决插口接触不良的问题
    CameraUpDownServoPinB = 9  # S3

    def __init__(self, ServoPin=23, pwm=50, mode="BCM"):
        # 忽略警告信息
        GPIO.setwarnings(False)
        self.set_mode(mode)

        self.ServoPin = ServoPin
        self.servo_init(pwm)


    def set_mode(self, mode="BCM"):
        if mode == "BCM":
            # 设置RGB三色灯为BCM编码方式
            GPIO.setmode(GPIO.BCM)

    def set_pin_model(self, pin, model=GPIO.OUT):
        # 设置pin的状态
        GPIO.setup(pin, model)

    # 舵机引脚设置为输出模式
    def servo_init(self, pwm):

        GPIO.setup(self.ServoPin, GPIO.OUT)
        # 设置pwm引脚和频率
        self.pwm_servo = GPIO.PWM(self.ServoPin, pwm)
        self.pwm_servo.start(0)

    def set_pin_model(self, model=GPIO.OUT):
        # 设置pin的状态
        GPIO.setup(self.ServoPin, model)

    def set_pwm(self, pwm=50):
        if self.pwm_servo is not None :
            self.pwm_servo.stop()
        # 设置pwm引脚和频率为?hz,默认2000hz
        # 设置pwm引脚和频率
        self.pwm_servo = GPIO.PWM(self.ServoPin, self.pwm)
        self.pwm_servo.start(0)

    def change_duty_cycle(self, cycle):
        self.pwm_servo.ChangeDutyCycle(cycle)

    def change_duty_cycle_by_angle(self, angle):
        self.pwm_servo.ChangeDutyCycle(2.5 + 10 * angle / 180)

    # 定义一个脉冲函数，用来模拟方式产生pwm值
    # 时基脉冲为20ms，该脉冲高电平部分在0.5-
    # 2.5ms控制0-180度
    def servo_pulse(self, angle):
        pulsewidth = (angle * 11) + 500
        GPIO.output(self.ServoPin, GPIO.HIGH)
        time.sleep(pulsewidth / 1000000.0)
        GPIO.output(self.ServoPin, GPIO.LOW)
        time.sleep(20.0 / 1000 - pulsewidth / 1000000.0)

    def servo_pulse1(self, angle):
        pulsewidth = angle
        GPIO.output(self.ServoPin, GPIO.HIGH)
        time.sleep(pulsewidth / 1000000.0)
        GPIO.output(self.ServoPin, GPIO.LOW)
        time.sleep(20.0 / 1000 - pulsewidth / 1000000.0)

    # 根据舵机脉冲控制范围为500-2500usec内：

    def servo_control(self, angle):
        if angle < 500:
            angle = 500
        elif angle > 2500:
            angle = 2500
        self.servo_pulse1(angle)

    def clean_pin_state(self,):
        self.pwm_servo.stop()
        GPIO.cleanup()



class KeyControl:
    # 小车按键定义
    key = 8

    def __init__(self, key, mode="BCM"):
        # 忽略警告信息
        GPIO.setwarnings(False)
        self.set_mode(mode)

        self.key = key

    def set_mode(self, mode="BCM"):
        if mode == "BCM":
            # 设置RGB三色灯为BCM编码方式
            GPIO.setmode(GPIO.BCM)

    # 按键检测
    def key_scan(self,delaytime):
        while GPIO.input(self.key):
            pass
        while not GPIO.input(self.key):
            time.sleep(delaytime)
            if not GPIO.input(self.key):
                time.sleep(delaytime)
                while not GPIO.input(self.key):
                    pass


class InfraredControl:

    # 红外避障引脚定义
    AvoidSensorLeft = 12
    AvoidSensorRight = 17

    def __init__(self, AvoidSensorLeft, AvoidSensorRight,mode="BCM"):
        # 忽略警告信息
        GPIO.setwarnings(False)
        self.set_mode(mode)

        self.AvoidSensorLeft = AvoidSensorLeft
        self.AvoidSensorRight = AvoidSensorRight

    def set_mode(self, mode="BCM"):
        if mode == "BCM":
            # 设置RGB三色灯为BCM编码方式
            GPIO.setmode(GPIO.BCM)

    def get_detect_val_of_both_side(self):
        return GPIO.input(self.AvoidSensorLeft),GPIO.input(self.AvoidSensorRight)

    def is_obstacle_on_right(self):
        LeftSensorValue,RightSensorValue =  self.get_detect_val_of_both_side()
        return LeftSensorValue == True and RightSensorValue == False

    def is_obstacle_on_left(self):
        LeftSensorValue, RightSensorValue = self.get_detect_val_of_both_side()
        return LeftSensorValue == False and RightSensorValue == True

    def is_obstacle_on_both_size(self):
        LeftSensorValue, RightSensorValue = self.get_detect_val_of_both_side()
        return LeftSensorValue == False and RightSensorValue == False

    def is_no_obstale_on_both_side(self):
        LeftSensorValue, RightSensorValue = self.get_detect_val_of_both_side()
        return LeftSensorValue == True and RightSensorValue == True

class LightFollowControl:

    # 光敏电阻引脚定义
    LdrSensorLeft = 7
    LdrSensorRight = 6

    def __init__(self, LdrSensorLeft, LdrSensorRight,mode="BCM"):
        # 忽略警告信息
        GPIO.setwarnings(False)
        self.set_mode(mode)

        self.LdrSensorLeft = LdrSensorLeft
        self.LdrSensorRight = LdrSensorRight

    def set_mode(self, mode="BCM"):
        if mode == "BCM":
            # 设置RGB三色灯为BCM编码方式
            GPIO.setmode(GPIO.BCM)

    def get_detect_val_of_both_side(self):
        return GPIO.input(self.LdrSensorLeft),GPIO.input(self.LdrSensorRight)

    def is_light_on_right(self):
        LdrSersorLeftValue,LdrSersorRightValue =  self.get_detect_val_of_both_size()
        return LdrSersorLeftValue == False and LdrSersorRightValue == True

    def is_light_on_left(self):
        LdrSersorLeftValue, LdrSersorRightValue = self.get_detect_val_of_both_size()
        return LdrSersorLeftValue == True and LdrSersorRightValue == False

    def is_light_on_both_side(self):
        LdrSersorLeftValue, LdrSersorRightValue = self.get_detect_val_of_both_size()
        return LdrSersorLeftValue == True and LdrSersorRightValue == True

    def is_no_light_on_both_side(self):
        LdrSersorLeftValue, LdrSersorRightValue = self.get_detect_val_of_both_size()
        return LdrSersorLeftValue == False and LdrSersorRightValue == False

class TrackingSensorControl:

    TrackSensorLeftPin1 = 3  # 定义左边第一个循迹红外传感器引脚为3口
    TrackSensorLeftPin2 = 5  # 定义左边第二个循迹红外传感器引脚为5口
    TrackSensorRightPin1 = 4  # 定义右边第一个循迹红外传感器引脚为4口
    TrackSensorRightPin2 = 18  # 定义右边第二个循迹红外传感器引脚为18口

    def __init__(self, TrackSensorLeftPin1, TrackSensorLeftPin2,TrackSensorRightPin1,TrackSensorRightPin2,mode="BCM"):
        # 忽略警告信息
        GPIO.setwarnings(False)
        self.set_mode(mode)

        self.TrackSensorLeftPin1 = TrackSensorLeftPin1
        self.TrackSensorLeftPin2 = TrackSensorLeftPin2
        self.TrackSensorRightPin1 = TrackSensorRightPin1
        self.TrackSensorRightPin2 = TrackSensorRightPin2

    def set_mode(self, mode="BCM"):
        if mode == "BCM":
            # 设置RGB三色灯为BCM编码方式
            GPIO.setmode(GPIO.BCM)

    def get_detect_val_of_tracking_sensor(self):
        return GPIO.input(self.TrackSensorLeftPin1),GPIO.input(self.TrackSensorLeftPin2)\
            ,GPIO.input(self.TrackSensorRightPin1),GPIO.input(self.TrackSensorRightPin2)

    # 四路循迹引脚电平状态
    # 0 0 X 0
    # 1 0 X 0
    # 0 1 X 0
    # 以上6种电平状态时小车原地右转
    # 处理右锐角和右直角的转动
    def is_right_actute_angle_or_right_angle(self):
        TrackSensorLeftValue1,TrackSensorLeftValue2,_,TrackSensorRightValue2 = self.get_detect_val_of_tracking_sensor()
        return (TrackSensorLeftValue1 == False or TrackSensorLeftValue2 == False) and TrackSensorRightValue2 == False


    # 四路循迹引脚电平状态
    # 0 X 0 0
    # 0 X 0 1
    # 0 X 1 0
    # 处理左锐角和左直角的转动
    def is_left_actute_angle_or_left_angle(self):
        TrackSensorLeftValue1,_,TrackSensorRightValue1,TrackSensorRightValue2 = self.get_detect_val_of_tracking_sensor()
        return TrackSensorLeftValue1 == False and (TrackSensorRightValue1 == False or TrackSensorRightValue2 == False)

    # 0 X X X
    # 最左边检测到
    def is_far_left_dectected(self):
        TrackSensorLeftValue1,_,_,_ = self.get_detect_val_of_tracking_sensor()
        return TrackSensorLeftValue1 == False


    # X X X 0
    # 最右边检测到
    def is_far_right_dectected(self):
        _,_,_,TrackSensorRightValue2 = self.get_detect_val_of_tracking_sensor()
        return TrackSensorRightValue2 == False

    # 四路循迹引脚电平状态
    # X 0 1 X
    # 处理左小弯
    def is_small_left_bend(self):
        _,TrackSensorLeftValue2,TrackSensorRightValue1,_ = self.get_detect_val_of_tracking_sensor()
        return TrackSensorLeftValue2 == False and TrackSensorRightValue1 == True

    # 四路循迹引脚电平状态
    # X 1 0 X
    # 处理右小弯
    def is_small_right_bend(self):
        _,TrackSensorLeftValue2,TrackSensorRightValue1,_ = self.get_detect_val_of_tracking_sensor()
        return TrackSensorLeftValue2 == True and TrackSensorRightValue1 == False

    # 四路循迹引脚电平状态
    # X 0 0 X
    # 处理直线
    def is_straight(self):
        _, TrackSensorLeftValue2, TrackSensorRightValue1, _ = self.get_detect_val_of_tracking_sensor()
        return TrackSensorLeftValue2 == False and TrackSensorRightValue1 == False

class ultrasonicControl:

    # 超声波引脚定义
    EchoPin = 0
    TrigPin = 1

    def __init__(self, EchoPin, TrigPin,mode="BCM"):
        # 忽略警告信息
        GPIO.setwarnings(False)
        self.set_mode(mode)

        self.EchoPin = EchoPin
        self.TrigPin = TrigPin

    def set_mode(self, mode="BCM"):
        if mode == "BCM":
            # 设置RGB三色灯为BCM编码方式
            GPIO.setmode(GPIO.BCM)

    def ultrasonic_init(self):
        GPIO.setup(self.EchoPin, GPIO.IN)
        GPIO.setup(self.TrigPin, GPIO.OUT)

    def distance(self):
        GPIO.output(self.TrigPin, GPIO.LOW)
        time.sleep(0.000002)
        GPIO.output(self.TrigPin, GPIO.HIGH)
        time.sleep(0.000015)
        GPIO.output(self.TrigPin, GPIO.LOW)

        t3 = time.time()
        while not GPIO.input(self.EchoPin):
            t4 = time.time()
            if (t4 - t3) > 0.03:
                return -1

        t1 = time.time()
        while GPIO.input(self.EchoPin):
            t5 = time.time()
            if (t5 - t1) > 0.03:
                return -1

        t2 = time.time()
        time.sleep(0.01)
        #    print "distance is %d " % (((t2 - t1)* 340 / 2) * 100)
        return ((t2 - t1) * 340 / 2) * 100

    def distance_detect(self):
        num = 0
        ultrasonic = []
        while num < 5:
            distance = self.distance()
            while int(distance) == -1:
                distance = self.distance()
                print("Tdistance is %f" % (distance))
            while (int(distance) >= 500 or int(distance) == 0):
                distance = self.distance()
                print("Edistance is %f" % (distance))
            ultrasonic.append(distance)
            num = num + 1
            time.sleep(0.01)
        print(ultrasonic)
        distance = (ultrasonic[1] + ultrasonic[2] + ultrasonic[3]) / 3
        print("distance is %f" % (distance))
        return distance

class BuzzerControl:

    # 蜂鸣器引脚定义
    buzzer = 8

    def __init__(self,buzzer,mode="BCM"):
        # 忽略警告信息
        GPIO.setwarnings(False)
        self.set_mode(mode)

        self.buzzer = buzzer
        self.buzzer_init()

    def set_mode(self, mode="BCM"):
        if mode == "BCM":
            # 设置RGB三色灯为BCM编码方式
            GPIO.setmode(GPIO.BCM)

    def buzzer_init(self):
        GPIO.setup(self.buzzer, GPIO.OUT, initial=GPIO.HIGH)

    def whistle(self, whistletime):
        GPIO.output(self.buzzer, GPIO.LOW)
        time.sleep(whistletime)
        GPIO.output(self.buzzer, GPIO.HIGH)
        time.sleep(0.001)

    def clean_pin_state(self,):
        GPIO.cleanup()


class OutFireControl:

    # 灭火电机引脚设置
    OutfirePin = 2

    def __init__(self, OutfirePin, mode="BCM"):
        # 忽略警告信息
        GPIO.setwarnings(False)
        self.set_mode(mode)

        self.OutfirePin = OutfirePin
        self.buzzer_init()

    def set_mode(self, mode="BCM"):
        if mode == "BCM":
            # 设置RGB三色灯为BCM编码方式
            GPIO.setmode(GPIO.BCM)

    def outfire_init(self):
        GPIO.setup(self.OutfirePin, GPIO.OUT, initial=GPIO.HIGH)

    def set_outfire_state(self,state=GPIO.LOW):
        GPIO.output(self.OutfirePin, state)

    def change_outfire_state(self):
        GPIO.output(self.OutfirePin, not GPIO.input(self.OutfirePin))

    def clean_pin_state(self, ):
        GPIO.cleanup()


