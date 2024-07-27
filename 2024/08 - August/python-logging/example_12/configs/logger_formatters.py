import json
import logging
from datetime import UTC, datetime


def serialize_local_timestamp(t: float) -> str | None:
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
