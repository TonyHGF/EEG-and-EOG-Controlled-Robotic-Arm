import time
import threading
import numpy as np
from pyOpenBCI import OpenBCICyton

# 定义一个阈值来检测眨眼事件，您可以根据实际数据进行调整
BLINK_THRESHOLD = 100  # 可以根据您的实际情况调整此值

# 定义一个列表来存储最近的样本数据
recent_samples = []

def detect_blink(sample):
    global recent_samples
    # 假设前额通道是通道 1（请根据实际情况调整）
    front_channel_data = sample.channels_data[0]

    # 将新的样本数据添加到最近的样本列表中
    recent_samples.append(front_channel_data)

    # 保持最近样本列表的长度不超过 250（1 秒的数据）
    if len(recent_samples) > 250:
        recent_samples.pop(0)

    # 计算最近样本的平均值
    mean_value = np.mean(recent_samples)

    # 检查当前样本是否超出阈值
    if abs(front_channel_data - mean_value) > BLINK_THRESHOLD:
        print(f"Blink detected at time: {time.time()}")

def print_data(sample):
    print(f"ID: {sample.id}")
    print(f"Channel Data: {sample.channels_data}")
    print(f"Timestamp: {time.time()}\n")
    detect_blink(sample)

def start_board_stream(board):
    board.start_stream(print_data)

# 替换为您的设备端口号
port = 'COM3'  # Windows 下的端口号
# port = '/dev/ttyUSB0'  # Linux 下的端口号

board = OpenBCICyton(port=port)

print("Starting the data stream...")
stream_thread = threading.Thread(target=start_board_stream, args=(board,))
stream_thread.start()

try:
    input("Press Enter to stop the data stream...\n")
except KeyboardInterrupt:
    pass

print("Stopping the data stream...")
board.stop_stream()
stream_thread.join()
