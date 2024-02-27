from multiprocessing import Pool
from random import randint, seed
from time import perf_counter, sleep


def func(a: int, b: int, *, upper_bound: int, job_id: int):
    print(f"Job #{job_id}: {a=}, {b=}, {job_id=}, {upper_bound=}")
    candidates = [False] * 2 + [True] * (upper_bound - 2)
    primes = []

    for i, isprime in enumerate(candidates):
        if isprime:
            primes.append(i)
            for n in range(i * i, upper_bound, i):
                candidates[n] = False

    return primes


def run_pool(job_size, pool_size):
    jobs = [
        (
            (i, i + 1),
            {
                "job_id": i,
                "upper_bound": randint(1_000_000, 10_000_000)
            }
        )
        for i in range(job_size)
    ]
    # kick off all the processes
    pool = Pool(processes=pool_size)

    async_results = [
        pool.apply_async(func, args=positionals, kwds=kwargs)
        for positionals, kwargs in jobs
    ]
    pool.close()

    # wait for async results to come back
    pool.join()

    # get all the results
    results = [result.get() for result in async_results]
    print(results[0])


if __name__ == "__main__":
    start = perf_counter()
    seed(0)
    run_pool(job_size=100, pool_size=10)
    print(f"Elapsed time: {perf_counter() - start:.2f}")
