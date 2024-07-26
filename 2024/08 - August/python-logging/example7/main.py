"""Example 7

In this example, we are going to customize the datetime output in our logs.

By default, the logging system uses **local** time (usually servers are configured in UTC, but your local
system probably is not. So, we'll want to somehow ensure that no matter what the local timezone is, the
logs records are **always** in UTC. Additionally, we'll change the serialization format to something other
than `2024-07-20 21:41:06,651`.

One way to do this is to specify this globally in the logging library, using the `logging.Formatter.converter`
attribute. We can set it to use the `gmtime` function in the `time` module. We could do this using pure
configuration, but I'm not going to do this because in addition I want to customize the format string.

For the actual formatting, we have to be a bit careful. The time converters (`time.localtime()` or `time.gmtime()` do
not provide fractional seconds. The logging library gets around this by actually defining two format strings,one
for the datetime at a seconds resolution, and a second format string just for the milliseconds.
We can override both those string at the logging library level using the `logging.Formatter.default_time_format` and
`logging.Formatter.default_msec_format` attributes.

There are other ways of doing this, but this is probably the simplest way to do it (that I'm aware of).

Note also that this method will affect all formatters, which is usually what we want. If you need to have different
formatters with different time formats, you'll have to do something more complicated, like creating a custom Formatter
subclass.
"""

import logging
import logging.config
import time

from yaml import safe_load

logger = logging.getLogger("app")


def configure_loggers():
    with open("logger_config.yaml") as f:
        config = safe_load(f)

    logging.Formatter.converter = time.gmtime
    logging.Formatter.default_time_format = "%Y-%m-%dT%H:%M:%S"
    logging.Formatter.default_msec_format = (
        "%s.%03dZ"  # we know times will be UTC, so we can hardcode the Z suffix
    )

    logging.config.dictConfig(config)


def main():
    logger.info("Info message")
    time.sleep(0.1)
    logger.error("Error message")


if __name__ == "__main__":
    configure_loggers()
    main()
