import math
import threading
from time import perf_counter


NUM_INTERVALS = 10_000_000
NUM_THREADS = 10_000
results = []


def func(x):
    # semi-circle, radius 1, centered at (0, 0)
    # integral from -1 to 1 of this function should gives us
    # the area of this semi-circle: pi / 2
    return math.sqrt(1 - x * x)


def riemann_sum(func, delta, a, i_start, i_end):
    # calculates the right Riemann sums
    area = 0
    for i in range(i_start, i_end):
        x = a + delta * i
        area += func(x) * delta
    results.append(area)


def split(num_intervals, n):
    k, m = divmod(num_intervals, n)
    return [(i * k + min(i, m), (i + 1) * k + min(i+1, m)) for i in range(n)]


if __name__ == '__main__':
    start = perf_counter()
    a = -1
    b = 1
    delta = (b - a) / NUM_INTERVALS

    # split the intervals into NUM_THREADS
    chunks = split(NUM_INTERVALS, NUM_THREADS)

    # Create the threads
    threads = []
    for i_start, i_end in chunks:
        threads.append(
            threading.Thread(target=riemann_sum, args=(func, delta, a, i_start, i_end))
        )

    # Start and join the threads
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    # all threads done processing - add all results up for final answer
    area = sum(results)

    end = perf_counter()
    print(f"Area: {area:.10f}, pi/2={math.pi / 2:.10f}")
    print(f"Elapsed: {end - start:.4f} seconds")