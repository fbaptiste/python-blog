"""Example 4

In this example we are going to set up a simple File handler.

Note that this file handler will just keep growing the log file over time, so you will need to
establish some process to purge it yourself.
"""

import logging
import logging.config

from yaml import safe_load

logger = logging.getLogger("app")


def configure_loggers():
    with open("logger_config.yaml") as f:
        config = safe_load(f)

    logging.config.dictConfig(config)


def main():
    logger.error("This is an error message: %s, %f.3f", "arg1", 0.333)
    logger.info("This is an info message")


if __name__ == "__main__":
    configure_loggers()
    main()
