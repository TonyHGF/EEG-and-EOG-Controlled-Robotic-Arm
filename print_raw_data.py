from pyOpenBCI import OpenBCICyton
import csv
import matplotlib.pyplot as plt
import numpy as np
import time

def print_raw(sample):
    print(sample.channels_data)

global filename
filename = "./data/eeg_read.csv"

def save_to_csv(sample):
    
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([sample.id] + sample.channels_data)

# def plot_csv(filename):
#     file_reader = csv.reader(open(filename))
#     data = list(file_reader)
#     rows = len(data)
#     row_len = len(data[0])

#     x = list()
#     y = list()

#     for i in range(1, rows):
#         x.append(data[i][0])
#         y.append(data[i])


def main():
    
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Sample Index'] + [f'Channel{i}'] for i in range(9))

    start_time = time.time()

    board = OpenBCICyton(port='COM5', daisy=False)

    board.start_stream(save_to_csv)


if __name__ == '__main__':
    main()


