"""GCP Helper Functions"""

import logging

logger = logging.getLogger(__name__)


def upload_file(source, target):
    logger.warning(
        "Uploading file using deprecated function",
        extra={"source": source, "target": target},
    )
