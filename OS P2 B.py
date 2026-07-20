from multiprocessing import Process, Queue
import random
import time

# Producer Function
def producer(queue):
    for i in range(5):
        item = random.randint(1, 100)

        if queue.full():
            print("Queue is FULL! No space available. Producer is waiting...")

        queue.put(item)   # Blocks if queue is full
        print(f"Producer produced: {item}")

        time.sleep(0.5)

# Consumer Function
def consumer(queue):

    # Delay so Producer fills the queue first
    time.sleep(3)

    for i in range(5):

        if queue.empty():
            print("Queue is EMPTY! Consumer is waiting...")

        item = queue.get()   # Blocks if queue is empty
        print(f"Consumer consumed: {item}")

        time.sleep(1)

# Main Program
if __name__ == "__main__":

    # Queue size = 3
    q = Queue(maxsize=3)

    # Create Processes
    p1 = Process(target=producer, args=(q,))
    p2 = Process(target=consumer, args=(q,))

    print("Starting Producer and Consumer...")

    # Start Processes
    p1.start()
    p2.start()

    # Wait for completion
    p1.join()
    p2.join()

    print("Producer and Consumer have finished.")
