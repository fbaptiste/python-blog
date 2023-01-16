"""Main app

This app pushes messages into the redis queue
"""
import random
from datetime import datetime
from json import dumps
from time import sleep
from uuid import uuid4

import redis

import config


def redis_db():
    db = redis.Redis(
        host=config.redis_host,
        port=config.redis_port,
        db=config.redis_db_number,
        password=config.redis_password,
        decode_responses=True,
    )

    # make sure redis is up and running
    db.ping()

    return db


def redis_queue_push(db, message):
    # push to tail of the queue (left of the list)
    db.lpush(config.redis_queue_name, message)



def main(num_messages: int, delay: float = 1):
    """
    Generates `num_messages` and pushes them to a Redis queue
    :param num_messages:
    :return:
    """

    # connect to Redis
    db = redis_db()

    for i in range(num_messages):
        # Create message data
        message = {
            "id": str(uuid4()),
            "ts": datetime.utcnow().isoformat(),
            "data": {
                "message_number": i,
                "x": random.randrange(0, 100),
                "y": random.randrange(0, 100),
            },
        }

        # We'll store the data as JSON in Redis
        message_json = dumps(message)

        # Push message to Redis queue
        print(f"Sending message {i+1} (id={message['id']})")
        redis_queue_push(db, message_json)

        # wait a bit so we have time to start up workers and see how things interact
        sleep(delay)



if __name__ == '__main__':
    main(30, 0.1)
