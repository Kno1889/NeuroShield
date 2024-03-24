from imu import MPU6050
from time import sleep
from machine import Pin, I2C
import math

max_accel = 0
# Shows Pi is on by turning on LED when plugged in
LED = Pin("LED", Pin.OUT)
LED.on()

i2c_1 = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
imu_1 = MPU6050(i2c_1)

i2c_2 = I2C(1, sda=Pin(2), scl=Pin(3), freq=400000)
imu_2 = MPU6050(i2c_2)

i2c_3 = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)
imu_3 = MPU6050(i2c_3)

i2c_4 = I2C(1, sda=Pin(6), scl=Pin(7), freq=400000)
imu_4 = MPU6050(i2c_4)


def get_accel(imu):
    A_x = round(imu.accel.x, 5)
    A_y = round(imu.accel.y, 5)
    A_z = round(imu.accel.z, 5)

    return math.sqrt(A_x**2 + A_y**2 + A_z**2)


while True:
    accel_1 = get_accel(imu_1)
    accel_2 = get_accel(imu_2)
    accel_3 = get_accel(imu_3)
    accel_4 = get_accel(imu_4)

    if accel_1 > max_accel:
        max_accel = accel_1

    if accel_2 > max_accel:
        max_accel = accel_2

    if accel_3 > max_accel:
        max_accel = accel_3

    if accel_4 > max_accel:
        max_accel = accel_4

    print("------------------------------")
    print(f"Magnitude 1: {accel_1}")
    print("\n")
    print(f"Magnitude 2: {accel_2}")
    print("\n")
    print(f"Magnitude 3: {accel_3}")
    print("\n")
    print(f"Magnitude 4: {accel_4}")
    print("\n")
    print(f"Max Acceleration: {max_accel}")
    print("------------------------------")
    print("\n")
    sleep(0.5)
