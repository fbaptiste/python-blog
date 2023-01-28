import queue
import random
import threading
from time import sleep


NUM_ITER = 100
counter = 0
sum_ = 0
c_lock = threading.Lock()
print_queue = queue.Queue()


def fuzz():
    sleep(random.random() / 10)


def print_queue_watcher():
    while True:
        item = print_queue.get()
        fuzz()
        print(item)
        fuzz()
        print_queue.task_done()
        fuzz()


def do_work():
    global counter
    global sum_

    fuzz()
    with c_lock:
        counter += 1
        next_sum = sum_ + counter
        print_queue.put(f"{sum_} + {counter} = {next_sum}")
        print_queue.put("-" * 20)
        sum_ = next_sum
    fuzz()


if __name__ == '__main__':
    threads = []

    # start daemon print watcher thread
    threading.Thread(target=print_queue_watcher, daemon=True).start()

    # create the threads
    for i in range(NUM_ITER):
        threads.append(threading.Thread(target=do_work))

    # start the threads with some fuzzing between starts
    for thread in threads:
        thread.start()
        fuzz()

    # wait until all threads are done
    for thread in threads:
        thread.join()

    # wait until the print queue is empty
    print_queue.join()

    print(f"DONE: solution = {sum_}")



