"""Example 11

In this example I just want to talk about what happens to our application when an exception occurs during logging.

As we are developing our application, this is fine - we definitely want to be aware of issues with our logging code.

But, when we move to production, we probably do not want an exception in our logging to affect the application itself.

We can tell the logging library to suppress these exceptions, and let our app continue running uninterrupted, by
setting a flag, at the library level: logging.raiseExceptions = False. Unfortunately, we this flag does not seem
to be supported in the dict config, so we have to do this in code (so we'd probably want to use an ENV var in order to easily
set it differently in various environments)

The app will continue running in both cases, but in the latter case, we won't see the
exception in the console. And if we are logging to that same console, then we are essentially "polluting" our logs.

To demonstrate this, I'm going to take the custom handler code we did in the last example, and introduce a bug.

We'll see how the application behaves, then we'll set that flag and see what changes.
"""

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
            "exceptionInfo": record.exc_info,
        }

        return json.dumps(log_dict)


def configure_loggers(raise_exceptions: bool = True):
    with open("logger_config.yaml") as f:
        config = safe_load(f)

    logging.config.dictConfig(config)
    logging.raiseExceptions = raise_exceptions


def main():
    try:
        raise ValueError("This is a test exception")
    except ValueError:
        logger.exception("An exception occurred", stack_info=True)

    logger.info("App continues running after logging exception")


if __name__ == "__main__":
    configure_loggers(raise_exceptions=False)
    main()
