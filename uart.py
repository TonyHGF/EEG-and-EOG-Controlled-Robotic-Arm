import serial
import time

# 配置串口参数
ser = serial.Serial(
    port='COM8',  # 根据实际情况修改端口号
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

# 确保串口已经打开
if ser.is_open:
    print("Serial port is open")

try:
    while True:
        # 发送数据
        ser.write(b'#000P1000T1500!\n')
        time.sleep(1)

        # 接收数据
        if ser.in_waiting > 0:
            rx_data = ser.readline().decode('utf-8').strip()
            print(f"Received data: {rx_data}")

        time.sleep(1)

except KeyboardInterrupt:
    print("Exiting program")

finally:
    ser.close()
    print("Serial port is closed")
    
