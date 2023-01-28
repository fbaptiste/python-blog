import math
from time import perf_counter


NUM_INTERVALS = 10_000_000


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
    return area


if __name__ == '__main__':
    start = perf_counter()
    a = -1
    b = 1
    delta = (b - a) / NUM_INTERVALS
    area = riemann_sum(func, delta, a, 0, NUM_INTERVALS)
    end = perf_counter()
    print(f"Area: {area:.10f}, pi/2={math.pi/2:.10f}")
    print(f"Elapsed: {end - start:.4f} seconds")
