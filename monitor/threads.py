import time
import random
from monitor import RWMonitor

def reader(monitor, reader_id, stop_event):
    while not stop_event.is_set():
        time.sleep(random.uniform(0.5, 2.0))
        monitor.request_read_access(reader_id)
        print(f"Leitor {reader_id} está LENDO...")
        time.sleep(random.uniform(0.1, 0.5))
        monitor.release_read_access(reader_id)

def writer(monitor, writer_id, stop_event):
    while not stop_event.is_set():
        time.sleep(random.uniform(1.0, 3.0))
        monitor.request_write_access(writer_id)
        print(f"Escritor {writer_id} está ESCREVENDO!!!")
        time.sleep(random.uniform(0.5, 1.5))
        monitor.release_write_access(writer_id)