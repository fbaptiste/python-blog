import logging
from datetime import datetime

from utils.loggers import inspect_logger

logger = logging.getLogger("utils")
inspect_logger("utils")


def format_date_standard(dt: datetime) -> str:
    inspect_logger("utils")
    logger.info("Formatting datetime", extra={"datetime": dt})
    return dt.strftime("%Y-%m-%d %H:%M:%S")
