import random
import threading
from time import sleep


NUM_ITER = 100
counter = 0
sum_ = 0
p_lock = threading.Lock()
c_lock = threading.Lock()


def fuzz():
    sleep(random.random() / 10)


def do_work():
    global counter
    global sum_

    fuzz()
    with c_lock:
        counter += 1
        curr_counter = counter
        prev_sum = sum_
        next_sum = sum_ + counter
        sum_ = next_sum
    fuzz()
    with p_lock:
        print(f"{prev_sum} + {curr_counter} = {next_sum}")
        print("-" * 20)
    fuzz()


if __name__ == '__main__':
    threads = []

    # create the threads
    for i in range(NUM_ITER):
        threads.append(threading.Thread(target=do_work))

    # start the threads
    for thread in threads:
        thread.start()

    # wait until all threads are done
    for thread in threads:
        thread.join()

    print(f"DONE: solution = {sum_}")
