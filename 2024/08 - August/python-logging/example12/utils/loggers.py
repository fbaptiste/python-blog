"""Some utility functions for loggers"""

import logging


def inspect_logger(name: str):
    if name not in logging.Logger.manager.loggerDict:
        print(f"Logger {name} not found")
    else:
        logger = logging.getLogger(name)
        print("-" * len(name))
        print(name)
        print("-" * len(name))
        print("Effective level: ", logger.getEffectiveLevel())
        print("Handlers:", logger.handlers)
        print("Disabled? ", logger.disabled)
        print("=" * len(name))
