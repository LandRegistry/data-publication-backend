import logging
import logging.handlers
from functools import wraps


class LoggerConfig(object):
    app = None
    _general = None

    def __init__(self, app):
        self.app = app

    def setup_logger(self, name):
        # create logger
        self._general = logging.getLogger(name)
        self._general.setLevel(_get_logging_level_from_string(self.app.config['LOGGING_LEVEL']))
        # create handler
        _general_handler = logging.handlers.TimedRotatingFileHandler(
            self.app.config['GENERAL_LOG_FILE'], when='midnight', utc=True)
        _general_handler.setLevel(_get_logging_level_from_string(self.app.config['LOGGING_LEVEL']))
        # create formatter
        _formatter = logging.Formatter(
            '%(asctime)s level=[%(levelname)s] logger=[%(name)s] message=[%(message)s] exception=[%(exc_info)s]',
            "%Y-%m-%d %H:%M:%S")
        # add formatter
        _general_handler.setFormatter(_formatter)
        # add handler to logger
        self._general.addHandler(_general_handler)

    def log(self, message, level="INFO", exception=None):
        msg_level = _get_logging_level_from_string(level)

        if self.app.config['LOGGING'] and self._general:
            self._general.log(level=msg_level, msg=message, exc_info=exception)

    def start_stop_logging(self, original_function):
        @wraps(original_function)
        def wrapped(*args, **kwargs):
            self.log("{} Start".format(original_function.__name__), level="DEBUG")
            original = original_function(*args, **kwargs)
            self.log("{} End".format(original_function.__name__), level="DEBUG")
            return original

        return wrapped

def _get_logging_level_from_string(level_text):
    """convert string to message level"""
    if level_text.upper() == "CRITICAL":
        level = logging.CRITICAL
    elif level_text.upper() == "ERROR":
        level = logging.ERROR
    elif level_text.upper() == "WARNING":
        level = logging.WARNING
    elif level_text.upper() == "DEBUG":
        level = logging.DEBUG
    else:
        level = logging.INFO
    return level
