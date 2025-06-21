import threading

#pra nao gerar tickets grandes demais
MAX_TICKET = 50

class RWMonitor:
    def __init__(self):
        self.lock = threading.Lock()
        self.readers_count = 0
        self.writer_active = False
        self.readers_can_enter = threading.Condition(self.lock)
        self.writers_can_enter = threading.Condition(self.lock)
        self.ticket_counter = 1
        self.queue = []  # [(ticket, 'reader'), (ticket, 'writer')]
            
    def request_read_access(self, reader_id):
        with self.lock:
            my_ticket = self.ticket_counter
            self.ticket_counter = (self.ticket_counter % MAX_TICKET) + 1
            self.queue.append((my_ticket, 'reader'))

            #espera ser o primeiro da fila e nao ter nenhum escritor ativo
            while self.queue[0][0] != my_ticket or self.writer_active:
                print(f"Leitor {reader_id} esperando. Ticket: {my_ticket}")
                self.readers_can_enter.wait()

            self.queue.pop(0)
            self.readers_count += 1
            print(f"Leitor {reader_id} ENTROU com ticket {my_ticket}. Leitores ativos: {self.readers_count}")
            
            #acorda todos os leitores consecutivos apos o leitor atual ate achar um leitor
            for i in range(len(self.queue)):
                ticket, tipo = self.queue[i]
                if tipo == 'reader':
                    self.readers_can_enter.notify()
                else:
                    break

    def release_read_access(self, reader_id):
        with self.lock:
            self.readers_count -= 1
            print(f"Leitor {reader_id} SAIU. Leitores restantes: {self.readers_count}")
            
            #se nao ha mais leitores, o proximo eh um escritor
            if self.readers_count == 0:
                self.writers_can_enter.notify()

    def request_write_access(self, writer_id):
        with self.lock:
            my_ticket = self.ticket_counter
            self.ticket_counter = (self.ticket_counter % MAX_TICKET) + 1
            self.queue.append((my_ticket, 'writer'))

            #espera ser o primeiro da fila, nao ter nenhum escritor ativo, nao ter nenhum leitor ativo
            while self.queue[0][0] != my_ticket or self.writer_active or self.readers_count > 0:
                print(f"Escritor {writer_id} esperando. Ticket: {my_ticket}")
                self.writers_can_enter.wait()

            self.queue.pop(0)
            self.writer_active = True
            print(f"Escritor {writer_id} ENTROU com ticket {my_ticket}.")

    def release_write_access(self, writer_id):
        with self.lock:
            self.writer_active = False
            print(f"Escritor {writer_id} SAIU.")
           
            #se a fila nao estiver vazia, acorda quem for o proximo dela
            if self.queue:
                next_type = self.queue[0][1]
                if next_type == 'writer':
                    self.writers_can_enter.notify()
                else:
                    self.readers_can_enter.notify()