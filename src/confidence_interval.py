import scipy.stats as st
import numpy as np


def generate_CI(data):
    return st.t.interval(0.95, len(data) - 1, loc=np.mean(data), scale=st.tstd(data))

def calculate_mean_std(data):
    return np.mean(data), np.std(data)


def read_time_data_from_CSV(folder_path: str):
    time = []
    for i in range(50):
        file_name = "/".join([folder_path, "seed_{}.csv".format(i)])
        with open(file_name, "r") as file:
            lines = file.readlines()
            time.append(float(lines[-1].split(",")[0]))
    # print(time)
    CI = generate_CI(time)
    mean, std = calculate_mean_std(time)
    print("CI={}, mean={}, std={}".format(CI, mean, std))
    return CI


if __name__ == "__main__":
    folder_path = "//"
    for i in range(4):
        print("door num={}".format(i + 1))
        CI = read_time_data_from_CSV(folder_path + "{}door".format(i + 1))


