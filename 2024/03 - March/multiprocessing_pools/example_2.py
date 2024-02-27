from multiprocessing import Pool
from random import randint, seed
from time import perf_counter, sleep


def sieve(upper_bound):
    print(f"running sieve: {upper_bound=}")
    candidates = [False] * 2 + [True] * (upper_bound - 2)
    primes = []

    for i, isprime in enumerate(candidates):
        if isprime:
            primes.append(i)
            for n in range(i*i, upper_bound, i):
                candidates[n] = False

    return primes


def run_pool(job_size, pool_size):
    jobs = [
        randint(1_000_000, 10_000_000)
        for i in range(job_size)
    ]
    # kick off all the processes
    with Pool(processes=pool_size) as pool:
        all_results = pool.map(sieve, jobs)

    # gather all results from all processes
    print(all_results[0])
    for result in all_results:
        print(f"number of primes found: {len(result)}")


if __name__ == "__main__":
    start = perf_counter()
    seed(0)
    run_pool(job_size=100, pool_size=10)
    print(f"Elapsed time: {perf_counter() - start:.2f}")
