"""Example 1

In this example we just create a root logger with no configuration, and log to that root logger, to see what happens.
Note: as I mentioned in the concepts video, we do not normally log to the root logger, but here I just want to show you
the default configuration for the root logger, as well as the "last resort" functionality.

The default configuration for the root logger is a WARNING level, and no handlers, with last resort turned on.
"""

import logging

# With last resort on (the default)
logger = logging.getLogger()

# Inspect root logger configuration
print(f"{logger.hasHandlers()=}")
print(f"{logger.getEffectiveLevel()=}, {logging.WARNING=}")

# Send various level log messages to the root logger
logger.debug("This is a debug message")
logger.info("This is an info message")
logger.warning("This is a warning message")
logger.error("This is an error message")
logger.critical("This is a critical message")


# Turn off last resort handler:
logging.lastResort = False
logger.warning("This is a warning message")
logger.error("This is an error message")
logger.critical("This is a critical message")
