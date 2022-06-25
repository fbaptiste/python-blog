"""This code defines the producer, which populates the work queue"""
import asyncio
from typing import List


async def produce_work(
    batch: List[dict], work_queue: asyncio.Queue, producer_completed: asyncio.Event
):
    """
    Puts all the requested work into the work queue.

    :param batch: list of all the params that were submitted to be processed (this is the list of
        dicts the main application sent over for processing)
    :param work_queue: main work queue that contains each individual task params
    :param producer_completed: event to indicate the producer has finished producing
        all requested work
    :return:
    """
    for data in batch:
        await work_queue.put(data)

    # finished putting all the data into the work queue - indicate we are done using
    # the producer_completed event
    producer_completed.set()
