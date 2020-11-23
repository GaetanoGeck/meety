import os

import pytest
import yaml

from meety import io
from meety.connect.handlers import Handlers


def load_data(path):
    path = ["test"] + path
    path = os.path.join(*path)
    with open(path) as yamlFile:
        return yaml.load(yamlFile, Loader=yaml.BaseLoader)


test_config = load_data(["connect", "test_handlers.yaml"])


@pytest.mark.parametrize("actions, order", [
    (c["actions"], c["order"]) for c in test_config
])
def test_handler(actions, order):
    """Compare cleaned dicts of loaded meetings with expected dicts."""
    if not actions:
        actions = []
    if not order:
        order = []

    handlers = Handlers()
    for action in actions:
        handlers.apply_action(action)

    expected = [
        (
            o["name"],
            o["command"],
            {
                "shell": io.str_is_true(o.get("shell", "False")),
            }
        )
        for o in order
    ]
    assert list(handlers.ordered) == expected
