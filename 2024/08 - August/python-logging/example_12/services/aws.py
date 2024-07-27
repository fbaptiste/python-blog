"""AWS Helper Functions"""

import logging

from utils.loggers import inspect_logger

logger = logging.getLogger(__name__)


def list_s3_bucket(bucket_name: str):
    inspect_logger(__name__)
    logger.debug("Listing bucket contents", extra={"bucketName": bucket_name})
