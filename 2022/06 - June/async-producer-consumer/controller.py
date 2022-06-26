"""Main Controller

This is the main controller that orchestrates the producer, the 'workers' (aka tasks),
sets up the various queues, and tracks when all work is completed to shut down everything
and issue the final job completed callback.
"""
import asyncio
from time import perf_counter
from typing import Callable, List

import consumer
import producer
import resulthandler


# some constants, but could be defined in a config file, or simply passed to run_job function when called
NUM_WORKERS = 25
WORK_QUEUE_MAX_SIZE = 100

NUM_RESULT_HANDLERS = 10
RESULT_QUEUE_MAX_SIZE = 100


async def _controller(
        batch: List[dict], task_completed_callback: Callable, job_completed_callback: Callable
) -> None:
    """
    This is the async controller.

    :param batch: a list of dictionaries received that defines the parameters for each task that has to run
    :param task_completed_callback: the callback to use when each task result becomes available
    :param job_completed_callback: the callback to use when the overall job is completed
    :return:
    """
    start = perf_counter()

    # create the work and result queues
    work_queue = asyncio.Queue(maxsize=WORK_QUEUE_MAX_SIZE)
    result_queue = asyncio.Queue(maxsize=RESULT_QUEUE_MAX_SIZE)

    # create a list of all the tasks that will need to run async
    tasks = []

    # Define the producer task, defining the event we'll look for when the producer is done
    producer_completed = asyncio.Event()
    producer_completed.clear()  # set the event status to False for starters
    tasks.append(
        asyncio.create_task(producer.produce_work(batch, work_queue, producer_completed))
    )

    # Create the worker (consumer) tasks
    for _ in range(NUM_WORKERS):
        tasks.append(
            asyncio.create_task(consumer.do_work(work_queue, result_queue))
        )

    # Create the result handler tasks
    for _ in range(NUM_RESULT_HANDLERS):
        tasks.append(
            asyncio.create_task(resulthandler.handle_task_result(result_queue, task_completed_callback))
        )

    # Now wait completion of producer, and kick off the consumers and result handlers
    await producer_completed.wait()
    await work_queue.join()
    await result_queue.join()

    # once we reach here, we're all done, so cancel all tasks
    for task in tasks:
        task.cancel()

    end = perf_counter()

    # all done, callback using the provided callback function
    job_completed_callback({"elapsed_secs": end - start})


def run_job(
    batch: List[dict], task_completed_callback: Callable, job_completed_callback: Callable
) -> None:
    """
    This is the function caller calls to kick off the job.
    Note that this function is not a coroutine - it's a standard function that will run the top-level
    entry point for our async processing.

    :param batch: a list of dictionaries received that defines the parameters for each task that has to run
    :param task_completed_callback: the callback to use when each task result becomes available
    :param job_completed_callback: the callback to use when the overall job is completed
    :return:
    """
    asyncio.run(_controller(batch, task_completed_callback, job_completed_callback))
