from pyOpenBCI import OpenBCICyton
import matplotlib.pyplot as plt
import numpy as np
import csv
import time

# Define the filename to save data
filename = "./data/eeg_read.csv"

# Initialize CSV file with headers
with open(filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Sample Index'] + [f'Channel {i+1}' for i in range(8)])

# Set up real-time plotting
plt.ion()
fig, ax = plt.subplots()
x = np.arange(0, 250)  # Adjust size as needed
y = np.zeros((8, 250))  # Adjust to number of channels
lines = [ax.plot(x, y[i, :])[0] for i in range(8)]

start_time = time.time()

def save_and_plot(sample):
    global y, start_time
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([sample.id] + sample.channels_data)
    
    y = np.roll(y, -1, axis=1)
    y[:, -1] = sample.channels_data
    
    for i in range(8):
        lines[i].set_ydata(y[i, :])
    plt.pause(0.01)
    
    if time.time() - start_time >= 1000:
        board.stop_stream()
        plt.ioff()
        plt.show()

# Create OpenBCI Cyton board object and start data stream
board = OpenBCICyton(port='COM5')  # Ensure to use the correct COM port
board.start_stream(save_and_plot)

# Wait for the stream to finish
while time.time() - start_time < 1000:
    time.sleep(0.1)