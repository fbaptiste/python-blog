"""App Configuration"""

import logging
import logging.config
import sys

from yaml import safe_load


def inspect_logger_disabling():
    # sourced from: https://stackoverflow.com/a/28694704
    @property
    def disabled(self):
        try:
            return self._disabled
        except AttributeError:
            return False

    @disabled.setter
    def disabled(self, disabled):
        if disabled:
            frame = sys._getframe(1)
            print(
                f"{frame.f_code.co_filename}:{frame.f_lineno} "
                f"disabled the {self.name} logger"
            )
        self._disabled = disabled

    logging.Logger.disabled = disabled


def configure_loggers(raise_exceptions: bool = True):
    with open("logger_config.yaml") as f:
        config = safe_load(f)

    logging.config.dictConfig(config)
    logging.raiseExceptions = raise_exceptions


inspect_logger_disabling()
