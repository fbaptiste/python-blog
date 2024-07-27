"""Example 8

In this example, we are going to look at how we can use the `extra` parameter.

Note that in this example, because of the way de configured our formatter's format string, that `extra`
dictionary **must** always contain the keys we use in the formatter. We'll come back to this later
in the context of structured logging and custom formatters
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
    logger.info("Info message", extra={"arg1": 100, "arg2": "test 1"})
    time.sleep(0.1)
    logger.error("Error message", extra={"arg1": 200, "arg2": "test 2"})


if __name__ == "__main__":
    configure_loggers()
    main()
