import threading
import time
import random
from collections import deque

# Semáforos e locks
mutex = threading.Lock()            # protege as variáveis globais
queue_sem = threading.Semaphore(1)  # protege a fila
read_try = threading.Semaphore(1)   # bloqueia leitores se escritor ativo ou aguardando
resource = threading.Semaphore(1)   # acesso exclusivo ao recurso para escritores

# Variáveis globais
read_count = 0
queue = deque()

def lendo(reader_id):
    print(f"[Reader {reader_id}] is READING...")
    time.sleep(random.uniform(0.2, 0.5))

def escrevendo(writer_id):
    print(f"[Writer {writer_id}] is WRITING...")
    time.sleep(random.uniform(0.3, 0.6))

def processo_leitor(reader_id):
    global read_count

    while True:
        # Entra na fila
        queue_sem.acquire()
        queue.append(threading.current_thread())
        print(f"[Reader {reader_id}] wants to enter and is WAITING.")
        queue_sem.release()

        # Espera sua vez na fila
        while True:
            queue_sem.acquire()
            if queue[0] == threading.current_thread():
                queue_sem.release()
                break
            queue_sem.release()
            time.sleep(0.01)

        # Controle de acesso dos leitores
        read_try.acquire()
        mutex.acquire()
        read_count += 1
        if read_count == 1:
            resource.acquire()
        mutex.release()
        read_try.release()

        # Sai da fila
        queue_sem.acquire()
        queue.popleft()
        queue_sem.release()

        print(f"[Reader {reader_id}] ENTERED and starts reading.")
        print(f"[Reader {reader_id}] Number of readers: {read_count}")
        lendo(reader_id)
        print(f"[Reader {reader_id}] finished reading and LEAVES.")

        # Finaliza leitura
        mutex.acquire()
        read_count -= 1
        if read_count == 0:
            resource.release()
        mutex.release()

        time.sleep(random.uniform(0.1, 0.4))

def processo_escritor(writer_id):
    while True:
        # Entra na fila
        queue_sem.acquire()
        queue.append(threading.current_thread())
        print(f"[Writer {writer_id}] wants to enter and is WAITING.")
        queue_sem.release()

        # Espera sua vez na fila
        while True:
            queue_sem.acquire()
            if queue[0] == threading.current_thread():
                queue_sem.release()
                break
            queue_sem.release()
            time.sleep(0.01)

        # Controle de acesso dos escritores
        read_try.acquire()
        resource.acquire()

        # Sai da fila
        queue_sem.acquire()
        queue.popleft()
        queue_sem.release()

        print(f"[Writer {writer_id}] ENTERED and starts writing.")
        escrevendo(writer_id)
        print(f"[Writer {writer_id}] finished writing and LEAVES.")

        resource.release()
        read_try.release()

        time.sleep(random.uniform(0.2, 0.5))

# Criação das threads
number_of_readers = 4
number_of_writers = 3
reader_threads = [threading.Thread(target=processo_leitor, args=(i,)) for i in range(number_of_readers)]
writer_threads = [threading.Thread(target=processo_escritor, args=(i,)) for i in range(number_of_writers)]

for t in reader_threads + writer_threads:
    t.daemon = True
    t.start()

# Executar por tempo limitado
time.sleep(12)
