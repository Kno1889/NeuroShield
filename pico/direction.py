import numpy as np

WINDOW_SIZE = 150
ACCEL_THRESHOLD = 1

def process_gyroscope_data(data_stream):
    
    max_x_index, max_y_index, min_x_index, min_y_index = None, None, None, None

    window = []

    for i, (x, y, z) in enumerate(data_stream):
        window.append((x, y, z))

        if len(window) == WINDOW_SIZE:
            window_array = np.array(window)
            
            max_x_index = np.argmax(window_array[:, 0])
            max_y_index = np.argmax(window_array[:, 1])
            min_x_index = np.argmin(window_array[:, 0])
            min_y_index = np.argmin(window_array[:, 1])

            max_x = window_array[max_x_index][0]
            max_y = window_array[max_y_index][1]
            min_x = window_array[min_x_index][0]
            min_y = window_array[min_y_index][1]

            window = []

            yield max_x_index, max_x, max_y_index, max_y, min_x_index, min_x, min_y_index, min_y


def get_data_stream(textfile_name: str):
    with open(textfile_name, "r") as f:
        lines = f.readlines()

        data_stream = [] # list of tuples

        for line in lines:
            coords = [] # tuple (x, y, z)
        
            for coord in line.split(", "):
                coords.append(float(coord.split(": ")[1]))

            data_stream.append(tuple(coords))

    return data_stream


def main():
    data_stream = get_data_stream("right.txt")

    for max_x_i, max_x, max_y_i, max_y, min_x_i, min_x, min_y_i, min_y in process_gyroscope_data(data_stream):
        print(f"Max X Index: {max_x_i}, Min X Index: {min_x_i}")
        print(f"Max X: {max_x}, Min X: {min_x}")
        
        print(f"Max Y Index: {max_y_i}, Min Y Index: {min_y_i}")
        print(f"Max Y: {max_y}, Min Y: {min_y}")

        if max_y_i < min_y_i and (max_y > ACCEL_THRESHOLD or min_y < -ACCEL_THRESHOLD): # crest in Y then trough => left
            print("left")

        elif min_y_i < max_y_i and (min_y < -ACCEL_THRESHOLD or max_y > ACCEL_THRESHOLD): # trough in Y then crest => right
            print("right")
        
        elif min_x_i < max_x_i and (min_x < -ACCEL_THRESHOLD or max_x > ACCEL_THRESHOLD):  # crest in X then trough => back
            print("back")
        
        elif max_x_i < min_x_i and (max_x > ACCEL_THRESHOLD or min_x < -ACCEL_THRESHOLD): # crest in X then trough => forward
            print("forward")
        else:
            print("Unsure/stable")


if __name__ == "__main__":
    main()