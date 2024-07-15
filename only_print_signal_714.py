import time
import threading
import csv
from queue import Empty
from pyOpenBCI import OpenBCICyton
import multiprocessing as mp

# 定义一个阈值来检测眨眼事件，您可以根据实际数据进行调整
BLINK_THRESHOLD = 100  # 可以根据您的实际情况调整此值

# 将 ADC 值转换为微伏值的缩放因子
adc_to_microvolts = 5 / (1 << 24)

def convert_signed_to_unsigned(signed_int):
    if signed_int < 0:
        unsigned_int = (1 << 24) + signed_int
    else:
        unsigned_int = signed_int
    return unsigned_int

def detect_blink(converted_data):
    # 假设前额通道是通道 1（请根据实际情况调整）
    front_channel_data = converted_data[0]
    # 检查当前样本是否超出阈值
    return abs(front_channel_data) > BLINK_THRESHOLD

def process_sample(sample, data_queue):
    try:
        # Convert signed data to unsigned and then to microvolts
        converted_data = [convert_signed_to_unsigned(ch) * adc_to_microvolts for ch in sample.channels_data]
        current_time = time.time()
        blink_detected = detect_blink(converted_data)
        data_queue.put((sample.id, converted_data, current_time, blink_detected))
    except Exception as e:
        print(f"Error processing sample: {e}")

def save_data(data_queue, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Sample Index'] + [f'Channel {i+1}' for i in range(8)] + ['Timestamp', 'Blink'])
        while True:
            try:
                sample_id, converted_data, current_time, blink_detected = data_queue.get()
                # Save data to CSV
                blink_marker = '*' if blink_detected else ''
                writer.writerow([sample_id] + converted_data + [current_time, blink_marker])
            except Exception as e:
                print(f"Error saving data: {e}")

def print_data(data_queue):
    while True:
        try:
            sample_id, converted_data, current_time, blink_detected = data_queue.get()
            blink_marker = '*' if blink_detected else ''
            print(f"Sample ID: {sample_id}, Data: {converted_data}, Time: {current_time}, Blink: {blink_marker}")
        except Empty:
            pass
        except Exception as e:
            print(f"Error printing data: {e}")

def start_board_stream(board, data_queue):
    try:
        board.start_stream(lambda sample: process_sample(sample, data_queue))
    except Exception as e:
        print(f"Error starting board stream: {e}")

def read_process(port, data_queue, filename):
    board = OpenBCICyton(port=port)
    print("Starting the data stream...")
    stream_thread = threading.Thread(target=start_board_stream, args=(board, data_queue))
    stream_thread.start()

    save_data_thread = threading.Thread(target=save_data, args=(data_queue, filename))
    save_data_thread.start()

    print_data_thread = threading.Thread(target=print_data, args=(data_queue,))
    print_data_thread.start()

    stream_thread.join()
    save_data_thread.join()
    print_data_thread.join()

if __name__ == "__main__":
    port = 'COM5'  # Windows 下的端口号
    filename = "../data/eeg_read.csv"
    data_queue = mp.Queue()

    read_proc = mp.Process(target=read_process, args=(port, data_queue, filename))

    read_proc.start()
    read_proc.join()
