import threading
import time
import random

# Semaphores
mutex = threading.Semaphore(1)
rw_mutex = threading.Semaphore(1)
queue = threading.Semaphore(1)

# Shared variables
read_count = 0
shared_data = 0


def reader(reader_id):
    global read_count

    time.sleep(random.uniform(0.1, 1))

    # Entry section
    queue.acquire()
    mutex.acquire()

    read_count += 1

    if read_count == 1:
        rw_mutex.acquire()

    mutex.release()
    queue.release()

    # Critical section
    print(f"Reader {reader_id} is reading. Shared Data = {shared_data}")
    time.sleep(random.uniform(0.1, 0.5))

    # Exit section
    mutex.acquire()

    read_count -= 1

    if read_count == 0:
        rw_mutex.release()

    mutex.release()


def writer(writer_id):
    global shared_data

    time.sleep(random.uniform(0.1, 1))

    # Entry section
    queue.acquire()
    rw_mutex.acquire()
    queue.release()

    # Critical section
    shared_data += 1

    print(f"Writer {writer_id} is writing. New Shared Data = {shared_data}")
    time.sleep(random.uniform(0.1, 0.5))

    # Exit section
    rw_mutex.release()


# Create reader and writer threads
reader_threads = [
    threading.Thread(target=reader, args=(i,))
    for i in range(3)
]

writer_threads = [
    threading.Thread(target=writer, args=(i,))
    for i in range(2)
]

# Start threads
for t in reader_threads + writer_threads:
    t.start()

# Wait for all threads to complete
for t in reader_threads + writer_threads:
    t.join()

print("All readers and writers have finished.")
