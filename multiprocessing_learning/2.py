from multiprocessing import Process, Queue

def read_and_process_signal(queue):
    while True:
        # 模拟读取硬件信号
        signal_data = "signal_data"
        print(f"Reading signal: {signal_data}")
        
        # 模拟数据处理
        processed_data = f"processed_{signal_data}"
        print(f"Processed data: {processed_data}")
        
        # 将处理后的数据放入队列
        queue.put(processed_data)

def generate_command_and_send(queue):
    while True:
        # 从队列中获取处理后的数据
        processed_data = queue.get()
        print(f"Received processed data: {processed_data}")
        
        # 根据处理结果生成指令
        command = f"command_based_on_{processed_data}"
        print(f"Generated command: {command}")
        
        # 模拟发送指令给另一个硬件
        print(f"Sending command: {command}")

if __name__ == "__main__":
    queue = Queue()
    
    # 创建进程
    p1 = Process(target=read_and_process_signal, args=(queue,))
    p2 = Process(target=generate_command_and_send, args=(queue,))
    
    # 启动进程
    p1.start()
    p2.start()
    
    # 等待进程完成
    p1.join()
    p2.join()
