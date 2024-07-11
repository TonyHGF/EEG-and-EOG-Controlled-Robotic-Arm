from pyOpenBCI import OpenBCICyton
import matplotlib.pyplot as plt
import numpy as np
import time


DATA_DIR = "../data/channels/"
WINDOW_SIZE = 1000  # Number of data points to display in the window
Y_LIM = (-1e7, 1e7)  # Adjust y-axis range as needed
PLOT_DURATION = 150  # Duration in seconds to run the plot
SAVE_INTERVAL = 0.3  # Save interval in seconds (300ms)

def save_np(sample):
    global y, start_time, save_time, board
    
    y = np.roll(y, -1, axis=1)
    y[:, -1] = sample.channels_data

    # save the data to a numpy file
    for i in range(8):
        np.save(f"{DATA_DIR}channel_{i+1}.npy", y[i, :])
    
    current_time = time.time() - start_time
    if current_time - save_time >= SAVE_INTERVAL:
        save_time = current_time
        print(f"Data saved at {current_time:.2f}s")

    if current_time >= PLOT_DURATION:
        board.stop_stream()
        

def main():
    board = OpenBCICyton(port='COM3')  # Ensure to use the correct COM port
    board.start_stream(save_np)

if __name__ == "__main__":
    # Initialize the y array to store the data
    y = np.zeros((8, WINDOW_SIZE))  # Adjust to number of channels
    start_time = time.time()
    save_time = start_time
    main()