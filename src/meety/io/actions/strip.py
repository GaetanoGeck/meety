from meety.io.actions import registry
from meety.io.actions.action import Action


class StripAction(Action):
    """Strips string in `texts` from attribute `key` in dictionary `d`.

    For example, `strip_action({1: 'foo-bar', 2: 'baz'}, 1, ['-'])`
    changes the dictionary to {1: 'foobar', 2: 'baz'}.
    """

    name = "strip"

    def __init__(self, key, texts):
        super().__init__()
        self._input = key
        if isinstance(texts, str):
            self._texts = [texts]
        else:
            self._texts = texts

    def is_applicable(self, data, current_level):
        return (
            super().is_applicable(data, current_level)
            and self._input in data.keys()
        )

    def _apply(self, data):
        value = data[self._input]
        for text in self._texts:
            value = value.replace(text, "")
        data[self._input] = value
        return data

    @classmethod
    def create(cls, data):
        input_ = data["input"]
        texts = data["texts"]
        return StripAction(input_, texts)

    @classmethod
    def register(cls):
        registry.register_action_class("strip", StripAction)
