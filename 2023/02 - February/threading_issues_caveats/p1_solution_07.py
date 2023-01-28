from time import perf_counter

NUM_ITER = 100_000
counter = 0
sum_ = 0


def do_work():
    global counter
    global sum_

    counter = counter + 1
    next_sum = sum_ + counter
    print(f"{sum_} + {counter} = {next_sum}")
    print("-" * 20)
    sum_ = next_sum


if __name__ == '__main__':
    start = perf_counter()
    for i in range(NUM_ITER):
        do_work()

    end = perf_counter()
    print(f"DONE: solution = {sum_}")
    print(f"elapsed: {end - start:.2f} seconds")
