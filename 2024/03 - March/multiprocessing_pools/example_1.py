from multiprocessing import Pool
from random import randint, seed
from time import perf_counter, sleep


def long_running_func(job_id, arg1, arg2, sleep_time):
    print(f"running job #{job_id} (sleep={sleep_time})")
    sleep(sleep_time)
    print(f"finished running job #{job_id}")
    return arg1 + arg2


def run_pool(job_size, pool_size):
    jobs = [
        (i, randint(1, 100), randint(1, 100), randint(1, 3))
        for i in range(job_size)
    ]
    # kick off all the processes
    with Pool(processes=pool_size) as pool:
        all_results = pool.starmap(long_running_func, jobs)

    # gather all results from all processes
    for result in all_results:
        print(result)


if __name__ == "__main__":
    start = perf_counter()
    seed(0)
    run_pool(job_size=50, pool_size=50)
    print(f"Elapsed time: {perf_counter() - start:.2f}")
