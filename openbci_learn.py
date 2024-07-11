import time
from pyOpenBCI import OpenBCICyton


def print_daisy_sample(sample):
    print(f"Daisy Sample ID: {sample.id}")
    print("Channel Data:")
    for i, channel in enumerate(sample.channels_data):
        print(f"  Channel {i + 1}: {channel}")
    print("Aux Data:")
    for i, aux in enumerate(sample.aux_data):
        print(f"  Aux {i + 1}: {aux}")
    # print(f"Timestamp: {sample.timestamp}")
    print(f"Board Type: {sample.board_type}")
    print("-" * 40)

# 创建 OpenBCICyton 对象，启用 Daisy 模块
board = OpenBCICyton(port='COM3', daisy=False)

# 开始数据流并使用新的回调函数
board.start_stream(print_daisy_sample)
