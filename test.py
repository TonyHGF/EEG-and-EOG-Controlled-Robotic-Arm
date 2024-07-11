from pyOpenBCI import OpenBCICyton
import numpy as np
import time
import os

# 定义每个通道的数据存储目录
channels_dirs = [f'../data/channel{i}' for i in range(1, 9)]

# 确保每个通道的目录都存在
for dir in channels_dirs:
    os.makedirs(dir, exist_ok=True)

last_save_time = time.time()

# def print_channel_data(sample):
#     global last_save_time
#     current_time = time.time()
#     if current_time - last_save_time >= 1:
#         # 对于每个通道
#         for i, channel_data in enumerate(sample.channels_data):
#             # 生成唯一的文件名
#             filename = f"data_{current_time}.npy"
#             # 构建完整的文件路径
#             filename = os.path.join(channels_dirs[i], filename)
#             # 将单个通道的数据保存为.npy文件
#             np.save(filename, np.array(channel_data))
#             print(f"Saved {filename}")
#         last_save_time = current_time

filename = "../data/eeg_read.csv"

# Initialize CSV file with headers
with open(filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Sample Index'] + [f'Channel {i+1}' for i in range(8)])


def check_blink(sample):



# 创建OpenBCIBoard实例
board = OpenBCICyton(port='COM3')

# 开始数据流，传入回调函数
board.start_stream()