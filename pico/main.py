# from ulab import numpy as np
from imu import MPU6050
from time import sleep
from machine import Pin, I2C
import math


WINDOW_SIZE = 30
ACCEL_THRESHOLD = 1
GYRO_THRESHOLD = 150

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
imu = MPU6050(i2c)
imu.accel_range = 1
imu.gyro_range = 2

DATA_WINDOW_X = []
DATA_WINDOW_Y = []

def process_gyroscope_data():

    max_x = max(DATA_WINDOW_X)
    min_x = min(DATA_WINDOW_X)

    max_y = max(DATA_WINDOW_Y)
    min_y = min(DATA_WINDOW_Y)
    
    max_x_i = DATA_WINDOW_X.index(max_x)
    min_x_i = DATA_WINDOW_X.index(min_x)
    
    max_y_i = DATA_WINDOW_Y.index(max_y)
    min_y_i = DATA_WINDOW_Y.index(min_y)

    # max_x_i = np.argmax(window_array[:, 0])
    # max_y_i = np.argmax(window_array[:, 1])
    # min_x_i = np.argmin(window_array[:, 0])
    # min_y_i = np.argmin(window_array[:, 1])

    # max_x = window_array[max_x_index][0]
    # max_y = window_array[max_y_index][1]
    # min_x = window_array[min_x_index][0]
    # min_y = window_array[min_y_index][1]

    determine_direction(max_x, max_y, min_x, min_y, max_x_i, max_y_i, min_x_i, min_y_i)

    return


def determine_direction(max_x, max_y, min_x, min_y, max_x_i, max_y_i, min_x_i, min_y_i):
    if max_y_i < min_y_i and (max_y > GYRO_THRESHOLD or min_y < -GYRO_THRESHOLD): # crest in Y then trough => Back
            print("Back")

    elif min_y_i < max_y_i and (min_y < -GYRO_THRESHOLD or max_y > GYRO_THRESHOLD): # trough in Y then crest => Forward
        print("Forward")
    
    elif min_x_i < max_x_i and (min_x < -GYRO_THRESHOLD or max_x > GYRO_THRESHOLD):  # trough in X then crest => back
        print("Right")
    
    elif max_x_i < min_x_i and (max_x > GYRO_THRESHOLD or min_x < -GYRO_THRESHOLD): # crest in X then trough => forward
        print("Left")
            
    return



def main():
    # constant monitoring
    # while(1):
    #     DATA_WINDOW.append((round(imu.gyro.x, 5), round(imu.gyro.y, 5), round(imu.gyro.z, 5)))

    #     if len(DATA_WINDOW) == WINDOW_SIZE:
    #         process_gyroscope_data()

    #         DATA_WINDOW = []
        
    #     sleep(0.01)

    while(1):
        # if math.sqrt(round(imu.gyro.x, 5) ** 2 + round(imu.gyro.y, 5) ** 2 + round(imu.gyro.z, 5) ** 2) >= GYRO_THRESHOLD:
        gyro_x = round(imu.gyro.x, 5)
        gyro_y = round(imu.gyro.y, 5)

        #print(f"X: {gyro_x}, Y: {gyro_y}")

        if ((abs(gyro_x) > GYRO_THRESHOLD) or (abs(gyro_y) > GYRO_THRESHOLD)):
            DATA_WINDOW_X.append(gyro_x)
            DATA_WINDOW_Y.append(gyro_y)

            if len(DATA_WINDOW_X) == WINDOW_SIZE:
                process_gyroscope_data()

                DATA_WINDOW_X.clear()
                DATA_WINDOW_Y.clear()

                exit(0)

            sleep(0.001)
        else:
            continue
    
    
    
    # for max_x_i, max_x, max_y_i, max_y, min_x_i, min_x, min_y_i, min_y in process_gyroscope_data(data_stream):
    #     print(f"Max X Index: {max_x_i}, Min X Index: {min_x_i}")
    #     print(f"Max X: {max_x}, Min X: {min_x}")
        
    #     print(f"Max Y Index: {max_y_i}, Min Y Index: {min_y_i}")
    #     print(f"Max Y: {max_y}, Min Y: {min_y}")

    #     


if __name__ == "__main__":
    main()