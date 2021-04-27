"""
Sets up some loggers for different situations


"""

import sys
import logging


USER_LOG_LEVEL = 19
DEV_LOG_LEVEL = 1


class DevFilter(logging.Filter):
    """
    This is really duplicating what I think is the basic functionality of the setLevel command in base Loggers,
    but going the 'obvious' route did not work.  If you can do the same thing in the canonical way, replace this!
    """

    _active_level = logging.WARNING

    def filter(self, record):
        return record.levelno >= self._active_level

    @classmethod
    def set_dev(cls, val):
        if val:
            cls._active_level = DEV_LOG_LEVEL
        else:
            cls._active_level = USER_LOG_LEVEL


class DevFormatter(logging.Formatter):
    """
    Use a more detailed printout in dev mode
    """

    DEV = "%(module)s.%(funcName)s(%(lineno)s):  %(message)s"
    USER = "  %(message)s"

    _use_dev = False

    def __init__(self):
        self.dev_formatter = logging.Formatter(self.DEV)
        self.user_formatter = logging.Formatter(self.USER)

    def format(self, record):
        if self._use_dev:
            return self.dev_formatter.format(record)
        else:
            return self.user_formatter.format(record)

    @classmethod
    def set_dev(cls, val):
        cls._use_dev = bool(val)


# log to the maya listener
Logger = logging.getLogger("mGui")
_listener_handler = logging.StreamHandler(sys.stdout)
_listener_handler.setFormatter(DevFormatter())
Logger.addHandler(_listener_handler)
Logger.propagate = False
Logger.setLevel(1)
Logger.addFilter(DevFilter())


def verbose(state):
    """
    if True, print all log messages; if not, print only INFO or higher.  Use the dev format when true and the plain
    format when false.
    """
    onoff = lambda p: "ON" if p else "OFF"
    sys.stdout.write("# verbose output is %s" % onoff(state))
    DevFilter.set_dev(state)
    DevFormatter.set_dev(state)


__all__ = ["Logger", "verbose"]
