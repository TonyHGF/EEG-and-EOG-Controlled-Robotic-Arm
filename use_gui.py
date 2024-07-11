import time
import threading
import numpy as np
import tkinter as tk
from tkinter import ttk
from pyOpenBCI import OpenBCICyton
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys

# 定义一个阈值来检测眨眼事件，您可以根据实际数据进行调整
BLINK_THRESHOLD = 100  # 可以根据您的实际情况调整此值

# 定义一个列表来存储最近的样本数据
recent_samples = []
channel_6_data = []  # 用于存储 channel 6 的数据
max_length = 600  # 数据窗口的最大长度

# 初始化基准值存储字典
baseline_values = {i: [] for i in range(8)}

def detect_blink(sample):
    global recent_samples
    # 假设前额通道是通道 1（请根据实际情况调整）
    front_channel_data = sample.channels_data[0]

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

def print_data(sample):
    global channel_6_data, baseline_values

    print(f"ID: {sample.id}")
    print(f"Channel Data: {sample.channels_data}")
    print(f"Timestamp: {time.time()}\n")
    detect_blink(sample)

    # 处理 channel 6 的数据
    channel_6 = sample.channels_data[5]  # 通道索引从 0 开始，因此 channel 6 是索引 5
    channel_6_data.append(channel_6)
    if len(channel_6_data) > max_length:
        channel_6_data.pop(0)
    update_plot()

    # 计算每个通道的基准值
    for i, value in enumerate(sample.channels_data):
        baseline_values[i].append(value)
        if len(baseline_values[i]) > max_length:
            baseline_values[i].pop(0)

    update_baseline_labels()

def update_plot():
    global channel_6_data, ax, canvas
    ax.clear()
    ax.plot(channel_6_data)
    ax.set_xlim(0, max_length)
    canvas.draw()

def update_baseline_labels():
    global baseline_values, baseline_labels
    for i in range(8):
        if len(baseline_values[i]) > 0:
            avg_value = np.mean(baseline_values[i])
            baseline_labels[i].config(text=f"Channel {i+1} Baseline: {avg_value:.2f}")

def start_board_stream(board):
    board.start_stream(print_data)

# 替换为您的设备端口号
port = 'COM3'  # Windows 下的端口号
# port = '/dev/ttyUSB0'  # Linux 下的端口号

def start_stream():
    global board
    board = OpenBCICyton(port=port)
    print("Starting the data stream...")
    stream_thread = threading.Thread(target=start_board_stream, args=(board,))
    stream_thread.start()
    return stream_thread

def stop_stream(thread):
    print("Stopping the data stream...")
    board.stop_stream()
    thread.join()

def on_start():
    global stream_thread
    stream_thread = start_stream()

def on_stop():
    stop_stream(stream_thread)
    root.quit()  # 退出 Tkinter 主循环
    sys.exit()   # 终止程序

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
fig = Figure(figsize=(8, 6))
ax = fig.add_subplot(111)

# 将 Matplotlib 图形嵌入到 Tkinter 界面中
canvas = FigureCanvasTkAgg(fig, master=frame)
canvas.get_tk_widget().grid(row=0, column=0, columnspan=2)

# 创建基准值标签
baseline_labels = []
for i in range(8):
    label = ttk.Label(frame, text=f"Channel {i+1} Baseline: N/A")
    label.grid(row=2+i, column=0, columnspan=2, sticky=(tk.W, tk.E))
    baseline_labels.append(label)

root.mainloop()
