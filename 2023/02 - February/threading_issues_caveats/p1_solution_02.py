import threading


NUM_ITER = 100
counter = 0
sum_ = 0


def do_work():
    global counter
    global sum_

    counter += 1
    next_sum = sum_ + counter
    print(f"{sum_} + {counter} = {next_sum}")
    print("-" * 20)
    sum_ = next_sum


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
