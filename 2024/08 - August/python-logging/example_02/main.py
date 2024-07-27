"""Example 2

In this example, we configure two loggers, the root logger and an app logger.

In our first configuration we do the following:
1. Define a console handler, and a custom string formatter
2. Attach that handler to the root logger only, and set that logger to DEBUG level.
3. Define the app logger, setting it's level to INFO, with no handlers, but with propagation turned on (the default)

When we do this, notice that debug logs do not show up in the console, whereas info and higher logs do.
This is because the app logger is set to INFO, so debug messages will be rejected by that logger. Higher levels
however, are accepted, and therefore propagate up to the root logger, where the console handler is attached.

Let's tweak our configuration a bit:
1. Change app logger level to DEBUG
So now, both the root logger and app logger are set to DEBUG level.
When we do this, notice that the debug logs now show up.

Let's tweak things a bit more:
1. Change root logger to WARNING.
So now, the root logger is set to INFO, and the app logger is set to DEBUG.
When we do this, any debug logs sent to the app **still** get handled by the root logger, this is because the app
logger already accepted the request and propagated it up the logger chain.

Finally, let's do one more tweak:
1. Change the app logger to disable propagation (`propagate: no` (or `false`, or `0`)

When we do this, we essentially are logging to a logger that has **no** handlers, and does not propagate, so
Python logging will automatically use the "last resort" logger, which is set to WARNING level, hence we only see
log messages with levels of WARNING and up.
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
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")


if __name__ == "__main__":
    configure_loggers()
    main()
