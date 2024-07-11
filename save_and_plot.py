
from pyOpenBCI import OpenBCICyton
import matplotlib.pyplot as plt
import numpy as np
import csv
import time

# Define the filename to save data
filename = "../data/eeg_read.csv"

# Initialize CSV file with headers
with open(filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Sample Index'] + [f'Channel {i+1}' for i in range(8)])

# Set up real-time plotting
plt.ion()
fig, ax = plt.subplots()
window_size = 1000  # Number of data points to display in the window
x = np.arange(0, window_size)  # Adjust size as needed
y = np.zeros((8, window_size))  # Adjust to number of channels
lines = [ax.plot(x, y[i, :])[0] for i in range(8)]

# Set the y-axis limits
ax.set_ylim(-1e2, 1e2)  # Adjust y-axis range as needed (example range for EEG data)

start_time = time.time()

def save_and_plot(sample):
    global y, start_time
    current_time = time.time() - start_time
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([sample.start_time] + sample.channels_data + [current_time])
    
    y = np.roll(y, -1, axis=1)
    y[:, -1] = sample.channels_data
    
    
    # print(y.shape)
    
    for i in range(8):
        print(y)
        lines[i].set_ydata(np.sign(y[i, :]) * np.log(np.abs(y[i, :]) + 1))
    
    ax.set_xlim(current_time - window_size / 250, current_time)
    plt.draw()
    # plt.pause(0.01)
    
    if current_time >= 150:
        board.stop_stream()
        plt.ioff()
        plt.show()


def check(sample):
    # 假设您已经有一个名为 sample 的 pyOpenBCI 的 Sample 对象
    print(dir(sample))

# Create OpenBCI Cyton board object and start data stream
board = OpenBCICyton(port='COM3')  # Ensure to use the correct COM port
board.start_stream(save_and_plot)
# board.start_stream(check)

# Wait for the stream to finish
while time.time() - start_time < 150:
    time.sleep(0.1)