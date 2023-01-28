import queue
import threading
from time import perf_counter

NUM_ITER = 100_000
counter = 0
sum_ = 0
c_lock = threading.Lock()
print_queue = queue.Queue()


def print_queue_watcher():
    while True:
        item = print_queue.get()
        print(item)
        print_queue.task_done()


def do_work():
    global counter
    global sum_

    with c_lock:
        counter += 1
        next_sum = sum_ + counter
        print_queue.put(f"{sum_} + {counter} = {next_sum}")
        print_queue.put("-" * 20)
        sum_ = next_sum


if __name__ == '__main__':
    start = perf_counter()
    threads = []

    # start daemon print watcher thread
    threading.Thread(target=print_queue_watcher, daemon=True).start()

    # create the threads
    for i in range(NUM_ITER):
        threads.append(threading.Thread(target=do_work))

    # start the threads with some fuzzing between starts
    for thread in threads:
        thread.start()

    # wait until all threads are done
    for thread in threads:
        thread.join()

    # wait until the print queue is empty
    print_queue.join()

    end = perf_counter()
    print(f"DONE: solution = {sum_}")
    print(f"elapsed: {end - start:.2f} seconds")



