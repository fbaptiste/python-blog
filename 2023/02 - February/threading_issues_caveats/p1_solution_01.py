NUM_ITER = 100
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
    for i in range(NUM_ITER):
        do_work()

    print(f"DONE: solution = {sum_}")
