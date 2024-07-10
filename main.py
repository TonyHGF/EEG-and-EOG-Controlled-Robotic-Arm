import threading
from monitor.realtime_eeg_monitor import realtime_eeg_monitor
from monitor.realtime_eeg_monitor import periodic_np_array_generator


if __name__ == "__main__":
    # Start the EEG monitoring in a separate thread
    monitoring_thread = threading.Thread(target=realtime_eeg_monitor, kwargs={
        'port': 'COM3',
        'duration': 150,
        'window_size': 1000,
        'y_axis_limit': (-1e7, 1e7)
    })
    monitoring_thread.start()

    # periodic_np_array_generator(interval=0.3)