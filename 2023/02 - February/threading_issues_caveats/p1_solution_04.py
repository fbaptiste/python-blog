import threading


NUM_ITER = 100
counter = 0
sum_ = 0
p_lock = threading.Lock()
c_lock = threading.Lock()


def do_work():
    global counter
    global sum_

    with c_lock:
        prev_sum = sum_
        counter += 1
        next_sum = sum_ + counter
        sum_ = next_sum

    with p_lock:
        print(f"{prev_sum} + {counter} = {next_sum}")
        print("-" * 20)


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
