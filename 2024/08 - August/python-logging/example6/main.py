"""Example 6

In this example, we are going to set up a system to log all our logs to a rotating file,
but also set things up, so that WARNING and higher logs will **also** log to the console.
Also, while we're at it, we'll use a file formatter to emit JSON strings. I'll use the printf syntax just
    to show how that works. As we'll see in this example, this approach to generating JSON is only partially
    adequate - things go off the rails when we log exceptions (so, if emitting JSON this way, do not log
    exceptions, as the stack trace is going to interfere with your output). We'll come back to this at a
    later time.
"""

import logging
import logging.config
import time

from yaml import safe_load

logger = logging.getLogger("app")


def configure_loggers():
    with open("logger_config.yaml") as f:
        config = safe_load(f)

    logging.config.dictConfig(config)


def main():
    logger.info("Info message")
    time.sleep(0.1)
    logger.error("Error message")

    time.sleep(0.1)
    try:
        raise ValueError("A value error occurred.")
    except ValueError:
        logger.exception("An exception occurred.")


if __name__ == "__main__":
    configure_loggers()
    main()
