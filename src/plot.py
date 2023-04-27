import matplotlib.pyplot as plt
import csv
from typing import List
from simulation import start_server_from_file
import numpy as np


def plot_average_moving_speed(time, average_speed, num, size):
    # extract first
    plt.plot(time, average_speed)
    plt.xlabel('Time')
    plt.ylabel('Average Speed')
    plt.title('Average Speed vs Time {}-{}'.format(num, size))
    # Show plot
    plt.show()

def plot_escape_people(time, people_remain):
    plt.plot(time, people_remain)
    plt.xlabel('Time')
    plt.ylabel('People Remain')
    plt.title('People Remain vs Time')
    # Show plot
    plt.show()
def read_data_from_csv(file_path: str):
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        data = []
        time = []
        people_remain = []
        average_speed = []

        for row in reader:
            numbers = [float(row[0]), int(row[1]), float(row[2])]
            # print(numbers)
            data.append(numbers)
            time.append(float(row[0]))
            people_remain.append(int(row[1]))
            average_speed.append(float(row[2]))

        return data, time, people_remain, average_speed


def generate_room_files_with_different_population(room_file: str, sizes: List):
    for size in sizes:
        with open(room_file, 'r') as original_file:
            lines = original_file.readlines()

        words = lines[16].split()
        words[1] = str(size)

        lines[16] = " ".join(words) + "\n"

        with open(str(size) + "_" + room_file, "w") as new_file:
            new_file.writelines(lines)

    # start_server_from_file('room1.txt', 'stat.csv')


# def exp_different_size_of_crowd(sizes: List, original_file):
    # generate_room_files_with_different_populaition(original_file, sizes)
    # for size in sizes:
    #     start_server_from_file(input_fname=str(size) + "_" + original_file, output_fname=str(size) + "_stat.csv",
    #                            display=False)
    # time_spent = []
    # for size in sizes:
    #     with open(str(size) + "_stat.csv", "r") as f:
    #         lines = f.readlines()
    #     words = lines[-1].split(",")
    #     time_spent.append(float(words[0]))
    # print(time_spent)
    # return time_spent


def get_numerical_result(file_name: str):
    time_spent = []
    with open(file_name, "r") as f:
        lines = f.readlines()
    words = lines[-1].split(",")
    time_spent.append(float(words[0]))
    return time_spent


if __name__ == "__main__":
    sizes = [i * 10 for i in range(1, 11)]
    door_num = [1,2,3,4]
    door_size = [30, 15]
    for size in door_size:
        current_data = []
        for num in door_num:
            file_name = str(num)+"door_width" + str(size)+"_300.csv"
            data, time, people_remain, average_speed = read_data_from_csv(file_name)
            # print("num_door={}, door_width={}, mean={}, std={}, time={}".format(
            #     num, size, np.mean(average_speed), np.std(average_speed), time[-1]
            # ))
            # plot_average_moving_speed(t, speed, num, size)
            current_data.append((time, people_remain))
            # print(speed[1:])
        fig, ax = plt.subplots()
        for i in range(4):
            ax.plot(current_data[i][0], current_data[i][1], label="door={}".format(i+1))
        ax.set_title('People Remain - Average Speed (door width={:.1f})'.format(float(size/10)))
        ax.set_xlabel('Time (second)')
        ax.set_ylabel('People')
        ax.legend()
        plt.show()
    # exp_different_size_of_crowd(sizes, "room1.txt")
    # generate_room_files_with_different_p
    # opulaition("room1.txt", sizes)
    # for size in sizes:
    #     start_server_from_file(input_fname=str(size) + "_room1.txt", output_fname=str(size) + "_stat.csv",
    #                            display=False)
    # time_spent = []
    # for size in sizes:
    #     with open(str(size) + "_stat.csv", "r") as f:
    #         lines = f.readlines()
    #     words = lines[-1].split(",")
    #     time_spent.append(float(words[0]))
    # print(time_spent)
    # data, time, average_speed = read_data_from_csv("./stat.csv")
    # plot_average_moving_speed(time, average_speed)
