"""Configuration for the command-line interface."""

import colorama
from termcolor import colored

from meety.logging import log

colorama.init()
STYLES = {}


def set_options(config):
    if not isinstance(config, dict):
        log.expected("dict", "cli", config)
    else:
        for k, v in config.items():
            _add_style(k, v)


def _add_style(style_name, style_def):
    if not isinstance(style_def, dict):
        log.expected("dict", "styles", style_def)
        return

    STYLES[style_name] = {
        key: style_def.get(key)
        for key in ["color", "background", "attrs"]
    }


def style(text, style_name="others"):
    style = STYLES.get(style_name) or {}
    return colored(
        text,
        style.get("color"),
        style.get("background"),
        attrs=style.get("attrs")
    )


def bf(text):
    return colored(text, attrs=["bold"])


def bf_str(datum):
    return bf(str(datum))
