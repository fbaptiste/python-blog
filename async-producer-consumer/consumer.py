"""The actual task 'worker' or 'processor' - the work queue consumer"""
import asyncio
from random import random
from time import perf_counter


async def do_work(work_queue: asyncio.Queue, result_queue: asyncio.Queue) -> None:
    """
    This function (coroutine) will perform the actual work, by pulling an item
    from the work queue, doing some work, and pushing the result
    to the result queue, and repeating indefinitely.

    This coroutine never terminates itself - it just keeps looking for work to
    do in the work_queue. It will instead be terminated by the controller when
    the controller decides all work has been done.

    :param work_queue: the work queue the task consumes (pulls from)
    :param result_queue: the result queue the task pushes a result to
        once the work is complete
    :return:
    """

    while True:
        # grab an item from the queue (if there is one)
        task_data = await work_queue.get()

        # read the data we need to perform the work
        task_id = task_data["task_id"]
        number = task_data["number"]

        # do some work that takes some time - simulated here with an async sleep
        start = perf_counter()
        await asyncio.sleep(random() * 2)  # random wait time up to 2 seconds
        result = number * number
        end = perf_counter()

        # push result to result queue
        await result_queue.put(
            {
                "task_id": task_id,
                "result": result,
                "time_secs": end - start
            }
        )

        # inform work queue the task is complete
        work_queue.task_done()
