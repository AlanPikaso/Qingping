from machine import Pin, PWM
import time
import _thread

# 初始化舵机PWM对象
servo = PWM(Pin(15), Pin.OUT)
servo.freq(50)  # 设置舵机频率为50Hz
servo.duty(180)  # 初始值应为正方向


def degree(a, b, c):  # 定义角度函数
    for i in range(a, b, c):
        servo.duty(i)
        time.sleep_ms(600)


# 初始化电机PWM对象
pwmA = PWM(Pin(27), Pin.OUT)  # 正转电机
pwmB = PWM(Pin(26), Pin.OUT)  # 反转电机
pwmA.freq(100)  # 设置正转电机频率为100Hz
pwmB.freq(100)  # 设置反转电机频率为100Hz
pwmA.duty(1023)  # 设置正转电机初始占空比最大值，全速
pwmB.duty(1)  # 此时电机全速运行


def B_speed(d, e, f):  # 定义控制反转电机速度的函数
    for j in range(d, e, f):
        pwmB.duty(j)  # 设置反转电机占空比，以改变速度
        time.sleep_ms(10)


def A_speed(l, m, n):  # 定义控制正转电机速度的函数
    for k in range(l, m, n):
        pwmA.duty(k)  # 设置反转电机占空比，以改变速度
        time.sleep_ms(50)


# 小车行驶代码：

# 第一个直角转弯
time.sleep_ms(5800)  # 进行持续5.8秒的直线行驶
thread_1 = _thread.start_new_thread(degree, (180, 60, -15))  # 开启第一个子线程下同，转弯
B_speed(0, 350, 10)  # 改变反转电机速度以减缓小车转弯时的速度
time.sleep_ms(14500)  # 以此状态运行14.5秒
thread_2 = _thread.start_new_thread(degree, (60, 180, 15))  # 回正小车
time.sleep(4)  # 等待主线程和子线程统一
B_speed(350, 1, -10)  # 过弯后加快小车速度
time.sleep_ms(7000)  # 沿相应轨道直线行驶7秒
A_speed(1023, 1, -10)  # 减速至小车停止运动，到达第一个停靠点

# 倒车入库
pwmB.duty(1023)  # 小车开始即全速倒车
thread_3 = _thread.start_new_thread(degree, (180, 60, -10))  # 调整角度进行倒车入库
time.sleep_ms(9300)  # 等待主线程和子线程统一
thread_4 = _thread.start_new_thread(degree, (60, 195, 25))  # 回正小车
A_speed(1, 1023, 6)  # 减速至完成入库

# 出库及第二个直角转弯
thread_5 = _thread.start_new_thread(degree, (160, 130, -15))  # 粗略调整角度
B_speed(1023, 450, -10)
time.sleep_ms(4900)  # 调整转弯时位置减少压线
thread_6 = _thread.start_new_thread(degree, (50, 60, 5))  # 加大转弯角度实现出库
B_speed(500, 1, -8)  # 出库同时进行加速，持续1.62秒
time.sleep_ms(1620)
thread_6 = _thread.start_new_thread(degree, (60, 180, 10))  # 回调角度摆正车身
A_speed(1023, 150, -10)  # 本行及下三行为减速停车，倒车，停车，目的在于调整车位置
B_speed(1, 850, 5)
time.sleep_ms(5600)
B_speed(850, 1, -5)
# 下几行代码同第一个直角转弯几乎相同，故不赘述
pwmA.duty(1023)
thread_7 = _thread.start_new_thread(degree, (180, 50, -15))  # 转弯
B_speed(0, 350, 10)  # 改变反转电机速度以减缓小车转弯时的速度
time.sleep_ms(12500)
thread_8 = _thread.start_new_thread(degree, (60, 180, 15))  # 回正
time.sleep(4)  # 等待主线程和子线程统一
B_speed(350, 0, -10)
time.sleep_ms(4000)  # 沿相应轨道直线行驶4秒
A_speed(1023, 1, -10)  # 此时小车停止运动,完成
