from contextlib import suppress

from meety.io.actions import registry
from meety.io.actions.action import Action


class InferAction(Action):
    """Adds entry `name` to dictionary if not already existent and if its
    value can be computed.

    For example, `infer_action({"id": "JohnDoe"}, "mail", "{id}@mail.com")`
    adds the key "mail" with value "JohneDoe@mail.com" to the dictionary.
    """

    name = "infer"

    def __init__(self, name, value):
        super().__init__()
        self._name = name
        self._value = value

    def is_applicable(self, data, current_level):
        return (
            super().is_applicable(data, current_level)
            and self._name not in data.keys()
        )

    def _apply(self, data):
        with suppress(KeyError):
            expanded = self._value.format_map(data)
            data[self._name] = expanded
        return data

    @classmethod
    def create(cls, data):
        name = data["name"]
        value = data["value"]
        return InferAction(name, value)

    @classmethod
    def register(cls):
        registry.register_action_class("infer", InferAction)
