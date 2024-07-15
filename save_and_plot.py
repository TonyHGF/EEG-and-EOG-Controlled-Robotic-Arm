import time
import threading
import numpy as np
import tkinter as tk
from tkinter import ttk
from queue import Empty
from pyOpenBCI import OpenBCICyton
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv
import sys
import multiprocessing as mp

# 定义一个阈值来检测眨眼事件，您可以根据实际数据进行调整
BLINK_THRESHOLD = 100  # 可以根据您的实际情况调整此值

# 将 ADC 值转换为微伏值的缩放因子
adc_to_microvolts = 5 * 1e6 / (1 << 24)

def convert_signed_to_unsigned(signed_int):
    if signed_int < 0:
        unsigned_int = (1 << 24) + signed_int
    else:
        unsigned_int = signed_int
    return unsigned_int

def detect_blink(sample):
    # 假设前额通道是通道 1（请根据实际情况调整）
    front_channel_data = sample.channels_data[0] * adc_to_microvolts
    # 检查当前样本是否超出阈值
    if abs(front_channel_data) > BLINK_THRESHOLD:
        print(f"Blink detected at time: {time.time()}")

def process_sample(sample, data_queue):
    # Convert signed data to unsigned and then to microvolts
    converted_data = [convert_signed_to_unsigned(ch) * adc_to_microvolts for ch in sample.channels_data]
    current_time = time.time()
    data_queue.put((sample.id, converted_data, current_time))

def save_data(data_queue, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Sample Index'] + [f'Channel {i+1}' for i in range(8)] + ['Timestamp'])
        while True:
            sample_id, converted_data, current_time = data_queue.get()
            # Save data to CSV
            writer.writerow([sample_id] + converted_data + [current_time])

def update_plot(data_queue, fig, ax, lines, canvas, window_size, y):
    try:
        while not data_queue.empty():
            sample_id, converted_data, current_time = data_queue.get_nowait()
            # Update the plot data
            y = np.roll(y, -1, axis=1)
            y[:, -1] = converted_data
            for i in range(8):
                lines[i].set_ydata(y[i, :])
            ax.set_xlim(current_time - window_size / 250, current_time)
        canvas.draw()
    except Empty:
        pass
    root.after(100, update_plot, data_queue, fig, ax, lines, canvas, window_size, y)

def start_board_stream(board, data_queue):
    board.start_stream(lambda sample: process_sample(sample, data_queue))

def plot_process(data_queue):
    global root
    # 设置实时绘图
    fig = Figure(figsize=(10, 6))
    ax = fig.add_subplot(111)
    window_size = 1000  # Number of data points to display in the window
    x = np.arange(0, window_size)  # Adjust size as needed
    y = np.zeros((8, window_size))  # Adjust to number of channels
    lines = [ax.plot(x, y[i, :])[0] for i in range(8)]

    # Set the y-axis limits
    ax.set_ylim(-250, 250)  # Adjust y-axis range as needed (example range for EEG data)

    # 创建 Tkinter 界面
    root = tk.Tk()
    root.title("OpenBCI GUI")

    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # 创建 Matplotlib 图形
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.get_tk_widget().grid(row=0, column=0, columnspan=2)

    # 定期更新绘图
    root.after(100, update_plot, data_queue, fig, ax, lines, canvas, window_size, y)

    root.mainloop()

def read_process(port, data_queue, filename):
    board = OpenBCICyton(port=port)
    print("Starting the data stream...")
    stream_thread = threading.Thread(target=start_board_stream, args=(board, data_queue))
    stream_thread.start()

    save_data_thread = threading.Thread(target=save_data, args=(data_queue, filename))
    save_data_thread.start()

    stream_thread.join()
    save_data_thread.join()

if __name__ == "__main__":
    port = 'COM5'  # Windows 下的端口号
    filename = "../data/eeg_read.csv"
    data_queue = mp.Queue()

    plot_proc = mp.Process(target=plot_process, args=(data_queue,))
    read_proc = mp.Process(target=read_process, args=(port, data_queue, filename))

    plot_proc.start()
    read_proc.start()

    plot_proc.join()
    read_proc.join()
