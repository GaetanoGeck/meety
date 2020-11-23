from abc import (
    ABC,
    abstractmethod,
)
from fnmatch import fnmatch

from meety.logging import log


class Action(ABC):
    def __init__(self):
        self._level = "*"

    def set_conditions(self, level_pattern):
        self._level = level_pattern

    def set_conditions_from_dict(self, data):
        self.set_conditions(data.get("level", "*"))

    def satisfies_conditions(self, current_level):
        return (
            current_level is None
            or fnmatch(str(current_level), self._level)
        )

    def is_applicable(self, data, current_level):
        return (
            isinstance(data, dict)
            and self.satisfies_conditions(current_level)
        )

    def apply(self, data, current_level=None):
        if not self.is_applicable(data, current_level):
            return data
        else:
            return self._do_apply(data)

    def _do_apply(self, data):
        try:
            self._apply(data)
        except KeyError as e:
            log.warning(
                f"Failed to apply action '{data}',"
                f" missing attribute '{e}'."
            )
        except Exception as e:
            log.warning(f"Failed to apply action '{data}'.")
            log.exception(e)
        finally:
            return data

    @abstractmethod
    def _apply(self, data):
        pass
