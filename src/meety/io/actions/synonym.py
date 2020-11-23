from fnmatch import fnmatch

from meety.io.actions import registry
from meety.io.actions.action import Action


class SynonymAction(Action):
    """Simplified version of `infer_action`, providing an entry under a
    new key.

    For example, `infer_action({"user": "JohnDoe"}, "name", ["user"])`
    replaces the key "user" by "name".
    """

    name = "synonym"

    def __init__(self, output, inputs):
        super().__init__()
        self._output = output
        self._inputs = inputs

    def is_applicable(self, data, current_level):
        return (
            super().is_applicable(data, current_level)
            and self._output not in data.keys()
        )

    def _apply(self, data):
        try:
            key = next(self._matching_keys(data))
        except StopIteration:
            pass
        else:
            data[self._output] = data[key]
            data.pop(key)
        finally:
            return data

    def _matching_keys(self, data):
        inputs = [inp.casefold() for inp in self._inputs]
        for input_pattern in inputs:
            for k in data.keys():
                if fnmatch(k, input_pattern):
                    yield k

    @classmethod
    def create(cls, data):
        output = data["output"]
        inputs = data["inputs"]
        return SynonymAction(output, inputs)

    @classmethod
    def register(cls):
        registry.register_action_class("synonym", SynonymAction)
