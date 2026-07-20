from multiprocessing import Process, Queue
import time
import random

# Producer Function
def producer(queue):
    for i in range(5):
        item = random.randint(1, 100)   # Generate a random item
        print(f"Producer produced: {item}")
        queue.put(item)                 # Put item into the queue
        time.sleep(random.random())     # Simulate production delay

# Consumer Function
def consumer(queue):
    for i in range(5):
        item = queue.get()              # Get item from the queue
        print(f"Consumer consumed: {item}")
        time.sleep(random.random())     # Simulate consumption delay

# Main Program
if __name__ == "__main__":
    q = Queue()   # Create a FIFO queue for communication

    # Create Producer and Consumer processes
    p1 = Process(target=producer, args=(q,))
    p2 = Process(target=consumer, args=(q,))

    # Start both processes
    p1.start()
    p2.start()

    # Wait for both processes to finish
    p1.join()
    p2.join()

    print("Producer and Consumer have finished.")
