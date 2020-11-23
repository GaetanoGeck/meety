import re

from meety.io.actions import registry
from meety.io.actions.action import Action


class ReplaceAction(Action):
    """Replace the value for the attribute with `key` if the value
    matches the expression and the substitute is defined by the
    dictionary attributes.
    """

    name = "replace"

    def __init__(self, key, expression, substitute):
        super().__init__()
        self._key = key
        self._pattern = re.compile(expression)
        self._substitute = substitute

    def is_applicable(self, data, current_level):
        return (
            super().is_applicable(data, current_level)
            and self._key in data.keys()
        )

    def _apply(self, data):
        value = data[self._key]
        template = self._pattern.sub(self._substitute, value)
        try:
            new_value = template.format_map(data)
        except KeyError:
            new_value = value
        finally:
            data[self._key] = new_value
        return data

    @classmethod
    def create(cls, data):
        input_ = data["input"]
        expression = data["expression"]
        substitute = data["substitute"]
        return ReplaceAction(input_, expression, substitute)

    @classmethod
    def register(cls):
        registry.register_action_class("replace", ReplaceAction)
