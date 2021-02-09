import pyperclip

from meety.io import (
    datetime,
    html,
)
from meety.io.actions import registry
from meety.io.utils import *


def reset_options():
    datetime.reset_options()
    registry.reset_options()


def set_options(config, name):
    datetime.set_options(config.get("preferences") or {}, name)
    registry.set_options(config.get("attributes") or [])


def split_on_semicolon_or_comma(text):
    if ";" in text:
        return text.split(";")
    return text.split(",")


def parse_first_possible(parser, tokens):
    for token in tokens:
        result = parser(token, False)
        if result and result.is_valid:
            return result
    return None


def process(data):
    data = process_recursively(data, _casefold_keys)
    for action in registry.get_actions():
        data = process_recursively(data, action)
    return data


def process_recursively(value, func, level=1):
    if isinstance(value, list):
        return func(
            [
                process_recursively(v, func, level+1)
                for v in value
            ],
            level
        )
    if isinstance(value, dict):
        return func(
            {
                k: process_recursively(v, func, level+1)
                for (k, v) in value.items()
            },
            level
        )
    else:
        return func(value, level)


def _casefold_keys(data, level):
    if isinstance(data, dict):
        return {
            k.casefold(): v
            for (k, v) in data.items()
        }
    return data


def copy_to_clipboard(text):
    pyperclip.copy(text)
