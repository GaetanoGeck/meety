import logging
import traceback

logging.basicConfig(format="%(levelname)s: %(message)s")


class MeetyLogger:
    ERROR = logging.ERROR
    WARNING = logging.WARNING
    INFO = logging.INFO
    DEBUG = logging.DEBUG

    LEVEL_NAMES = {
        ERROR: "Error",
        WARNING: "Warning",
        INFO: "Info",
        DEBUG: "Debug",
    }

    def __init__(self):
        self._logger = logging.getLogger()
        self._contents = []

    def setDebug(self):
        self._logger.setLevel(logging.DEBUG)

    def setInfo(self):
        self._logger.setLevel(logging.INFO)

    def setWarn(self):
        self._logger.setLevel(logging.WARN)

    def setError(self):
        self._logger.setLevel(logging.ERROR)

    def debug(self, message, condition=True):
        if not condition:
            return
        self._logger.debug(message)
        self._add(logging.DEBUG, message)

    def info(self, message, condition=True):
        if not condition:
            return
        self._logger.info(message)
        self._add(logging.INFO, message)

    def warning(self, message, condition=True):
        if not condition:
            return
        self._logger.warning(message)
        self._add(logging.WARNING, message)

    def error(self, message, condition=True):
        if not condition:
            return
        self._logger.error(message)
        self._add(logging.ERROR, message)

    def exception(self, ex, warn=True):
        msg = f"Exception: {ex}"
        if warn:
            self._logger.warning(msg)
        else:
            self._logger.debug(msg)
        self._logger.debug(traceback.format_exc())

    def propagate(self, flag):
        self._logger.propagate = flag

    def expected(self, what, name, data, error=False):
        text = (
            f"Ignoring data '{data}' for '{name}' "
            f"where {what} was expected."
        )
        if error:
            self.error(text)
        else:
            self.warning(text)

    def print_stack(self):
        traceback.print_stack()

    @classmethod
    def level_name(cls, level):
        return cls.LEVEL_NAMES[level]

    def contents(self, level=logging.WARNING):
        return [(lev, msg) for (lev, msg) in self._contents if lev >= level]

    def _add(self, level, message):
        self._contents.append((level, message))


log = MeetyLogger()
