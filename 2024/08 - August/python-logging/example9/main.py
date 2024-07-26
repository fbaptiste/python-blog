"""Example 9

In this example we'll look at how to create custom filters.

We'll set up two handlers, one of which will look for some value in the `extra` dictionary, and only handle the log
record if that value satisfies some condition.

Specifically we are going to configure our logger this way:
1. App logger will be set to WARNING
2. App logger wil have two handlers, the "regular" handler which will log all
  log records it receives (INFO and up), and a "special" handler, which will
  only handle WARNING and higher levels, as well as check that some value(s) in the `extra`
  data meet some condition(s) before it will handle the log.

The custom filter needs to be defined in Python code, that's not something we can
specify in the configuration, but we will make a reference to it in the config when we attach it
to the specific handler. Side note, you can also attach filters to the logger itself, using the same
approach, just setting the configuration at the logger level instead of the handler level.

This example also shows how we can pass filter configuration values from the YAML config file to the filter class
when it gets instantiated by the logging system.

You'll see in the configuration file that we use something weird in the filter definition: `()`.
This is meant to be a hint to the logging system that it should instantiate the class, and pass the
configuration.
This is documented here: https://docs.python.org/3/library/logging.config.html#user-defined-objects
"""

import logging
import logging.config

from yaml import safe_load

logger = logging.getLogger("app")


class CustomFilter(logging.Filter):
    def __init__(self, arg_name: str = None, arg_threshold: int = None):
        self.arg_name = arg_name
        self.arg_threshold = arg_threshold

    def filter(self, record: logging.LogRecord):  # noqa: A003
        # Here we look for the arg attribute. If the attribute is present, and it's value
        # is > self.arg_threshold, then we allow the record to be processed (return True),
        # otherwise we filter it out (return False)
        return (
            self.arg_name
            and self.arg_threshold
            and hasattr(record, self.arg_name)
            and getattr(record, self.arg_name) > self.arg_threshold
        )


def configure_loggers():
    with open("logger_config.yaml") as f:
        config = safe_load(f)

    logging.config.dictConfig(config)


def main():
    logger.error("Error message 1, my_arg not specified")
    logger.error("Error message 2, my_arg=200", extra={"my_arg": 200})
    logger.error("Error message 3, my_arg=50", extra={"my_arg": 50})


if __name__ == "__main__":
    configure_loggers()
    main()
