import time
import threading
import numpy as np
import tkinter as tk
from tkinter import ttk
from queue import Queue, Empty
from pyOpenBCI import OpenBCICyton
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv
import sys

# 定义一个阈值来检测眨眼事件，您可以根据实际数据进行调整
BLINK_THRESHOLD = 100  # 可以根据您的实际情况调整此值

# 定义一个列表来存储最近的样本数据
recent_samples = []
channel_6_data = []  # 用于存储 channel 6 的数据
max_length = 250  # 数据窗口的最大长度

# 初始化基准值存储字典
baseline_values = {i: [] for i in range(8)}

# 将 ADC 值转换为微伏值的缩放因子
adc_to_microvolts = 5 * 1e6 / (1 << 24)

def convert_signed_to_unsigned(signed_int):
    if signed_int < 0:
        unsigned_int = (1 << 24) + signed_int
    else:
        unsigned_int = signed_int
    return unsigned_int

def detect_blink(sample):
    global recent_samples
    # 假设前额通道是通道 1（请根据实际情况调整）
    front_channel_data = sample.channels_data[0] * adc_to_microvolts

    # 将新的样本数据添加到最近的样本列表中
    recent_samples.append(front_channel_data)

    # 保持最近样本列表的长度不超过 250（1 秒的数据）
    if len(recent_samples) > max_length:
        recent_samples.pop(0)

    # 计算最近样本的平均值
    mean_value = np.mean(recent_samples)

    # 检查当前样本是否超出阈值
    if abs(front_channel_data - mean_value) > BLINK_THRESHOLD:
        print(f"Blink detected at time: {time.time()}")

def process_sample(sample, data_queue):
    # Convert signed data to unsigned and then to microvolts
    converted_data = [convert_signed_to_unsigned(ch) * adc_to_microvolts for ch in sample.channels_data]
    current_time = time.time() - start_time
    data_queue.put((sample.id, converted_data, current_time))

def save_data(data_queue):
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        while True:
            try:
                sample_id, converted_data, current_time = data_queue.get(timeout=1)
                # Save data to CSV
                writer.writerow([sample_id] + converted_data + [current_time])
            except Empty:
                continue

def update_plot():
    global y
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
    root.after(100, update_plot)

def start_board_stream(board, data_queue):
    board.start_stream(lambda sample: process_sample(sample, data_queue))

# 替换为您的设备端口号
port = 'COM5'  # Windows 下的端口号

def start_stream():
    global board, data_queue, start_time
    data_queue = Queue()
    board = OpenBCICyton(port=port)
    print("Starting the data stream...")
    stream_thread = threading.Thread(target=start_board_stream, args=(board, data_queue))
    stream_thread.start()

    # Start the thread to save data
    save_data_thread = threading.Thread(target=save_data, args=(data_queue,))
    save_data_thread.start()

    start_time = time.time()

    return stream_thread, save_data_thread

def stop_stream(threads):
    print("Stopping the data stream...")
    for thread in threads:
        thread.join()

def on_start():
    global stream_threads
    stream_threads = start_stream()

def on_stop():
    stop_stream(stream_threads)
    root.quit()  # 退出 Tkinter 主循环
    sys.exit()   # 终止程序

# 定义 CSV 文件名
filename = "../data/eeg_read.csv"

# 初始化 CSV 文件头
with open(filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Sample Index'] + [f'Channel {i+1}' for i in range(8)] + ['Timestamp'])

# 设置实时绘图
fig = Figure(figsize=(10, 6))
ax = fig.add_subplot(111)
window_size = 1000  # Number of data points to display in the window
x = np.arange(0, window_size)  # Adjust size as needed
y = np.zeros((8, window_size))  # Adjust to number of channels
lines = [ax.plot(x, y[i, :])[0] for i in range(8)]

# Set the y-axis limits
ax.set_ylim(-250, 250)  # Adjust y-axis range as needed (example range for EEG data)

start_time = time.time()

# 创建 Tkinter 界面
root = tk.Tk()
root.title("OpenBCI GUI")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

start_button = ttk.Button(frame, text="Start", command=on_start)
start_button.grid(row=1, column=0, padx=5, pady=5)

stop_button = ttk.Button(frame, text="Stop", command=on_stop)
stop_button.grid(row=1, column=1, padx=5, pady=5)

# 创建 Matplotlib 图形
canvas = FigureCanvasTkAgg(fig, master=frame)
canvas.get_tk_widget().grid(row=0, column=0, columnspan=2)

# 创建基准值标签
baseline_labels = []
for i in range(8):
    label = ttk.Label(frame, text=f"Channel {i+1} Baseline: N/A")
    label.grid(row=2+i, column=0, columnspan=2, sticky=(tk.W, tk.E))
    baseline_labels.append(label)

# 定期更新绘图
root.after(100, update_plot)

root.mainloop()
