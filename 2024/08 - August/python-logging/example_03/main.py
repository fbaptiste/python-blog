"""Example 3

In this example we are going to configure our loggers the same way we did in Example 2, but we'll use cde instead of
a config dict.

Notice how the app logger is a singleton object.
"""

import logging
import sys


def configure_loggers():
    root_logger = logging.getLogger()
    app_logger = logging.getLogger("app")
    print(f"app logger id: {hex(id(app_logger))}")

    stream_handler = logging.StreamHandler(stream=sys.stdout)
    simple_formatter = logging.Formatter(
        "SIMPLE FORMATTER: {asctime} - {name} - {levelname} - {message}",
        style="{",
    )
    stream_handler.setFormatter(simple_formatter)
    root_logger.addHandler(stream_handler)
    root_logger.setLevel(logging.DEBUG)

    app_logger.setLevel(logging.INFO)


def main():
    logger = logging.getLogger("app")
    print(f"app logger id: {hex(id(logger))}")
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")


if __name__ == "__main__":
    configure_loggers()
    main()
