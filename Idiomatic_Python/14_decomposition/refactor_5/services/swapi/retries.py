"""Utilities for a timeout retry decorator"""
from requests.exceptions import Timeout, RequestException


def timeout_retry(max_attempts, initial_timeout):
    """
    Decorator factory that abstracts out timeout retry logic.

    :param max_attempts: maximum number of attempts
    :param initial_timeout: the initial timeout, gets doubled if query times out
    :return: decorator function
    """
    attempt_number = 1
    current_timeout = initial_timeout

    def decorator(fn):
        def inner(*args, **kwargs):
            nonlocal attempt_number
            nonlocal current_timeout

            while True:
                try:
                    print(f"\tattempt #{attempt_number}")
                    result = fn(*args, **kwargs, timeout=current_timeout)

                    return result
                except Timeout:
                    if attempt_number >= max_attempts:
                        # reached max number of attempts
                        raise RequestException("Max attempts exceeded")
                    attempt_number += 1
                    current_timeout *= 2
                    print(f"\t\tRequest timed out. Trying again with a longer timeout ({current_timeout} s).")

        return inner
    return decorator


