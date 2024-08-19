"""Example 10

In this example we'll look at how to write a custom formatter.

We'll go back to our previous JSON formatter, but this time we'll make it a bit more complex
and give it the ability to handle exceptions properly.

Note that you do have 3rd party libraries that will do this, and a lot more, for you.

For example the structlog library is a very powerful library that can handle structured logging. Slightly simpler
alternatives exist too, that just focus on a JSON formatter - but, like libraries in general, they need to cater
to a wide range of use cases, and so can be a bit more complex than what you need.

Here, I want to do things from first principles, so we understand what's going on under the hood.
Once you do, then feel free to use those 3rd party libraries.

Also, to be completely honest, I rarely need the advanced functionality these 3rd party libraries provide,
and often, for me at least, simpler is better. One less library to learn, one less set of unverified code
included in my code base (do you really check that the library you are using is safe??), and one less thing that
can go wrong or functionality that gets deprecated over time. Basically, if I can implement a piece of functionality
quickly and effectively, I'll do it myself, rather than rely on a library. Enough with the soapbox!
"""

import inspect
import json
import logging
import logging.config
from datetime import UTC, datetime

from yaml import safe_load

logger = logging.getLogger("app")


def serialize_local_timestamp(t: float) -> str:
    dt = datetime.fromtimestamp(t, UTC)
    return dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")


class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord):  # noqa: A003
        # Create a dictionary that gathers all the info we want to log
        # We'll need to make sure whatever we gather is JSON serializable (or
        #   we can alternatively create a custom JSON encoder)
        # We could even leverage Pydantic to do this for us, especially if we already use Pydantic
        #   in our application. But let's keep it simple, and just see how custom formatters work.

        # Notes:
        # The attribute record.message is the raw (non-interpolated message string). Instead, we use
        #   .getMessage() to have the log record return the interpolated message string.
        # The log creation time is available in record.created, which is a float representing the time in
        #   seconds, but as a local time. We can convert this to UTC and with whatever string serialization we want.
        # We'll want to serialize the exception info and stack trace, and although the record provides us that info,
        # we would need to serialize that ourselves - instead, we can use the Formatter class's built-in methods
        # formatException() and formatStack() to do this for us.

        log_dict = {
            "time": serialize_local_timestamp(record.created),
            "loggerName": record.name,
            "levelName": record.levelname,
            "levelNumber": record.levelno,
            "message": record.getMessage(),
            "module": record.module,
            "filename": record.filename,
            "filePath": record.pathname,
            "funcName": record.funcName,
            "exceptionInfo": (
                self.formatException(record.exc_info)
                if record.exc_info
                else None
            ),
            "stackTrace": (
                self.formatStack(record.stack_info)
                if record.stack_info
                else None
            ),

        }

        # Identify attributes that were passed in extras - no direct way to do this, so we'll
        # compare what a regular log record without any extras looks like, and identify keys
        # in the current log record that are not present in the plain-vanilla log record.
        blank_record = logging.LogRecord("", 0, "", 0, "", (), None)
        standard_fields = {key for key, _ in inspect.getmembers(blank_record)}
        for key, value in inspect.getmembers(record):
            if key not in standard_fields:
                log_dict[key] = value

        return json.dumps(log_dict)


def configure_loggers():
    with open("logger_config.yaml") as f:
        config = safe_load(f)

    logging.config.dictConfig(config)


def main():
    logger.info("Message 1")
    logger.info("Message 2: val=%s", "value")
    logger.error("Message 3", extra={"a": 1, "b": 2, "c": 3})

    try:
        raise ValueError("This is a test exception")
    except ValueError:
        logger.exception("An exception occurred", stack_info=True)


if __name__ == "__main__":
    configure_loggers()
    main()
