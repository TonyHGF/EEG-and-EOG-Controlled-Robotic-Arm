import time
from pyOpenBCI import OpenBCICyton

def print_data(sample):
    print(f"ID: {sample.id}")
    print(f"Channel Data: {sample.channels_data}")
    print(f"Timestamp: {time.time()}\n")

# 替换为您的设备端口号
port = 'COM3'  # Windows 下的端口号

board = OpenBCICyton(port=port)

print("Starting the data stream...")
board.start_stream(print_data)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopping the data stream...")
    board.stop_stream()
