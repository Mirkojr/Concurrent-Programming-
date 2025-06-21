Pseudocógido para a solução usando semáforos 

```c

semaphore mutex = 1;
semaphore queue_sem = 1;
semaphore read_try = 1;
semaphore resource = 1;

int read_count = 0;
queue Q;


void processo_leitor(int reader_id) {
    while (true) {
        P(queue_sem);
        Q.push(current_thread);
        V(queue_sem);

        while (true) {
            P(queue_sem);
            if (Q.front() == current_thread) {
                V(queue_sem);
                break;
            }
            V(queue_sem);
        }

        P(read_try);
        P(mutex);
        read_count++;
        if (read_count == 1) {
            P(resource);
        }
        V(mutex);
        V(read_try);

        P(queue_sem);
        Q.pop();
        V(queue_sem);

        lendo(reader_id);

        P(mutex);
        read_count--;
        if (read_count == 0) {
            V(resource);
        }
        V(mutex);

        sleep_random();
    }
}

void processo_escritor(int writer_id) {
    while (true) {
        P(queue_sem);
        Q.push(current_thread);
        V(queue_sem);

        while (true) {
            P(queue_sem);
            if (Q.front() == current_thread) {
                V(queue_sem);
                break;
            }
            V(queue_sem);
            sleep_short();
        }

        P(read_try);
        P(resource);

        P(queue_sem);
        Q.pop();
        V(queue_sem);

        escrevendo(writer_id);

        V(resource);
        V(read_try);

        sleep_random();
    }
}
```
