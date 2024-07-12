import threading

def task1():
    cnt1 = 0
    while True:
        print("Task 1 is running", cnt1)
        cnt1 += 1
        # 可以加一些交互逻辑，例如队列、管道等

def task2():
    cnt2 = 0
    while True:
        print("Task 2 is running", cnt2)
        cnt2 += 1
        # 可以加一些交互逻辑，例如队列、管道等

# 创建线程
t1 = threading.Thread(target=task1)
t2 = threading.Thread(target=task2)

# 启动线程
t1.start()
t2.start()

# 等待线程完成
t1.join()
t2.join()
