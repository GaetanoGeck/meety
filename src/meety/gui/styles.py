"""Configuration for the graphical user interface."""

from meety.io import utils
from meety.logging import log

STYLES = {}
ATTRIBUTES = [
    "show",
    "size",
    "color",
    "background",
    "selected",
    "attrs",
]
DEFAULTS = {
    "show": "yes",
    "size": "18",
    "color": "black",
    "background": "white",
    "selected": "white",
    "attrs": [],
}


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
    STYLES[style_name] = {key: style_def.get(key) for key in ATTRIBUTES}


def get_style_value(style_name, value):
    return STYLES.get(style_name).get(value) or DEFAULTS.get(value)


def get_show(style_name="others"):
    return utils.str_is_true(get_style_value(style_name, "show"))


def get_color(style_name="others"):
    return get_style_value(style_name, "color")


def get_background(style_name="others"):
    return get_style_value(style_name, "background")


def get_selected(style_name="others"):
    return get_style_value(style_name, "selected")


def get_attrs(style_name="others"):
    return get_style_value(style_name, "attrs")


def get_font_size(style_name="others"):
    return int(get_style_value(style_name, "size"))


def is_bold(style_name="others"):
    return "bold" in get_attrs(style_name)


def get_border_color():
    return "#aaa"
