import threading
import time
from monitor import RWMonitor
from threads import reader, writer

def main():
    stop_event = threading.Event()
    monitor = RWMonitor()

    num_readers = 5
    num_writers = 2

    reader_threads = []
    writer_threads = []

    for i in range(num_readers):
        t = threading.Thread(target=reader, args=(monitor, i + 1, stop_event))
        reader_threads.append(t)
        t.start()

    for i in range(num_writers):
        t = threading.Thread(target=writer, args=(monitor, i + 1, stop_event))
        writer_threads.append(t)
        t.start()

    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("\nEncerrando programa")
        stop_event.set()

        for t in reader_threads + writer_threads:
            t.join(timeout=2)

        print("Programa finalizado com sucesso.")

if __name__ == "__main__":
    main()