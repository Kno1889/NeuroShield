# from ulab import numpy as np
from imu import MPU6050
from time import sleep
from machine import Pin, I2C
import math
#from enum import Enum

WINDOW_SIZE = 75
ACCEL_THRESHOLD = 2
GYRO_THRESHOLD = 100

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
imu = MPU6050(i2c)
imu.accel_range = 1
imu.gyro_range = 2

DATA_WINDOW_X = []
DATA_WINDOW_Y = []
DATA_WINDOW_ACCEL = []

#class ImpactDirection(Enum):
#    UNDETERMINED = 0
#    BACK = 1
#    FRONT = 2
#    RIGHT = 3
#    LEFT = 4


def process_gyroscope_data():

    max_x = max(DATA_WINDOW_X)
    min_x = min(DATA_WINDOW_X)

    max_y = max(DATA_WINDOW_Y)
    min_y = min(DATA_WINDOW_Y)
    
    max_x_i = DATA_WINDOW_X.index(max_x)
    min_x_i = DATA_WINDOW_X.index(min_x)
    
    max_y_i = DATA_WINDOW_Y.index(max_y)
    min_y_i = DATA_WINDOW_Y.index(min_y)

    return determine_direction(max_x, max_y, min_x, min_y, max_x_i, max_y_i, min_x_i, min_y_i)


def determine_direction(max_x: float, max_y: float, min_x: float, min_y: float, max_x_i: int, max_y_i: int, min_x_i: int, min_y_i: int):
    if max_y_i < min_y_i and (max_y > GYRO_THRESHOLD or min_y < -GYRO_THRESHOLD): # crest in Y then trough => Back
        # print("Back")
        return 1

    elif min_y_i < max_y_i and (min_y < -GYRO_THRESHOLD or max_y > GYRO_THRESHOLD): # trough in Y then crest => Forward
        # print("Front")
        return 2

    elif min_x_i < max_x_i and (min_x < -GYRO_THRESHOLD or max_x > GYRO_THRESHOLD):  # trough in X then crest => back
        # print("Right")
        return 3
    
    elif max_x_i < min_x_i and (max_x > GYRO_THRESHOLD or min_x < -GYRO_THRESHOLD): # crest in X then trough => forward
        # print("Left")
        return 4
    
def send_to_app(inst_accel: float, gyro_x: float, gyro_y: float, gyro_z: float, peak_accel: float, impact_direction = None):
    # send all this data via bluetooth\
    print(f"Accel: {inst_accel}, Gyro: <{gyro_x}, {gyro_y}, {gyro_z}>, Peak Accel: {peak_accel}, Impact Dir: {impact_direction}")
    return

def process_accelerometer_data():
    return max(DATA_WINDOW_ACCEL)
            

def main():

    start = False

    while(1):
        accel_x = round(imu.accel.x, 2)
        accel_y = round(imu.accel.y, 2)
        accel_z = round(imu.accel.z, 2)
        accel_magn = math.sqrt(accel_x ** 2 + accel_y ** 2 + accel_z ** 2)

        gyro_x = round(imu.gyro.x, 2)
        gyro_y = round(imu.gyro.y, 2)
        gyro_z = round(imu.gyro.z, 2)

        impact_direction = 0
        max_accel = 0

        # if ((abs(gyro_x) > GYRO_THRESHOLD) or (abs(gyro_y) > GYRO_THRESHOLD)):
        #     start = True

        if (accel_magn > ACCEL_THRESHOLD):
            start = True
        
        if (start):
            DATA_WINDOW_X.append(gyro_x)
            DATA_WINDOW_Y.append(gyro_y)

            DATA_WINDOW_ACCEL.append(accel_magn)
            

            if len(DATA_WINDOW_X) == WINDOW_SIZE:
                impact_direction = process_gyroscope_data()
                max_accel = process_accelerometer_data()

                DATA_WINDOW_X.clear()
                DATA_WINDOW_Y.clear()
                
                start = False
                
                sleep(1)
        
        send_to_app(accel_magn, gyro_x, gyro_y, gyro_z, max_accel, impact_direction)

        sleep(0.001)
    

if __name__ == "__main__":
    main()