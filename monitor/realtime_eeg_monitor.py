from pyOpenBCI import OpenBCICyton
import matplotlib.pyplot as plt
import numpy as np
import csv
import time
from datetime import datetime
import os

def realtime_eeg_monitor(port='COM3', duration=15, window_size=1000, y_axis_limit=(-1000, 1000)):
    """
    Function to monitor EEG signals in real-time and save data to a CSV file.

    Parameters:
    port (str): The COM port for the OpenBCI Cyton board.
    duration (int): Duration in seconds for the monitoring.
    window_size (int): Number of data points to display in the window.
    y_axis_limit (tuple): Y-axis limits for the EEG plots.
    """
    # Define the filename to save data: eeg_data_date_time
    dir = '../data'
    filename = f"eeg_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    filename = os.path.join(dir, filename)

    # Initialize CSV file with headers
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Sample Index'] + [f'Channel {i+1}' for i in range(8)])

    # Set up real-time plotting
    plt.ion()
    fig, axs = plt.subplots(8, 1, figsize=(10, 15))  # 8 subplots for 8 channels
    x = np.arange(0, window_size)
    y = np.zeros((8, window_size))  # Adjust to number of channels
    lines = [axs[i].plot(x, y[i, :])[0] for i in range(8)]

    # Set the y-axis limits for all subplots
    for ax in axs:
        ax.set_ylim(y_axis_limit)

    start_time = time.time()

    def save_and_plot(sample):
        nonlocal y, start_time
        current_time = time.time() - start_time
        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([sample.id] + sample.channels_data)
        
        y = np.roll(y, -1, axis=1)
        y[:, -1] = sample.channels_data
        
        for i in range(8):
            lines[i].set_ydata(y[i, :])
            axs[i].set_xlim(max(0, current_time - window_size / 250), current_time)
        
        plt.draw()
        plt.pause(0.01)
        
        if current_time >= duration:
            board.stop_stream()
            plt.ioff()
            plt.show()

    # Create OpenBCI Cyton board object and start data stream
    board = OpenBCICyton(port=port)  # Ensure to use the correct COM port
    board.start_stream(save_and_plot)

    # Wait for the stream to finish
    while time.time() - start_time < duration:
        time.sleep(0.1)

def periodic_np_array_generator(interval=0.3):
    """
    Function to generate and transmit NumPy array files every given interval.

    Parameters:
    interval (float): Time interval in seconds between generating files.
    """
    while True:
        time.sleep(interval)
        current_data = np.copy(y)  # Assuming y is the current EEG data array
        dir = '../data/'
        filename = f'eeg_data_{datetime.now().strftime("%Y%m%d_%H%M%S_%f")}.npy'
        file_path = os.path.join(dir, filename)
        # np.save(filename, current_data)
        np.save(file_path, current_data)
        # Implement the transmission logic here


