import threading
import time
import random

SIZE = 5
buffer = [None] * SIZE

in_pos = 0
out_pos = 0

mutex = threading.Lock()
empty = threading.Semaphore(SIZE)
full = threading.Semaphore(0)


def producer():
    global in_pos

    for i in range(10):
        item = random.randint(1, 100)

        empty.acquire()
        mutex.acquire()

        buffer[in_pos] = item
        print("Produced:", item)

        in_pos = (in_pos + 1) % SIZE

        mutex.release()
        full.release()

        time.sleep(0.5)


def consumer():
    global out_pos

    for i in range(10):

        full.acquire()
        mutex.acquire()

        item = buffer[out_pos]
        print("Consumed:", item)

        out_pos = (out_pos + 1) % SIZE

        mutex.release()
        empty.release()

        time.sleep(1)


if __name__ == "__main__":

    print("Producer-Consumer Bounded Buffer")

    p = threading.Thread(target=producer)
    c = threading.Thread(target=consumer)

    p.start()
    c.start()

    p.join()
    c.join()

    print("Program Completed")
