"""Azure Helper Functions"""

import logging

logger = logging.getLogger(__name__)


def get_sql_server_connection():
    logger.info("Getting SQL server connection")
