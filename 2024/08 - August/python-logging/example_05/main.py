"""Example 5

In this example, we are going to set up a rotating file handler. We'll do a size based handler
with a ridiculously small size in order to see the rotation happening quickly.

As you can see, as the log files fill up they are renamed with an appended number, and only 3 of the
"old" log files are retained. The current log file is always named "app.log", as we set in our config.
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
    for i in range(100):
        logger.info("Info message #%i", i)


if __name__ == "__main__":
    configure_loggers()
    main()
