"""Configuration for the graphical user interface."""

from meety.logging import log

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
        for key in ["color", "background", "selected", "attrs"]
    }


def get_style(style_name):
    return STYLES.get(style_name) or {}


def get_color(style_name="others"):
    return get_style(style_name).get("color") or "black"


def get_background(style_name="others"):
    return get_style(style_name).get("background") or "white"


def get_selected(style_name="others"):
    return get_style(style_name).get("selected") or "white"


def get_attrs(style_name="others"):
    return get_style(style_name).get("attrs") or []


def is_bold(style_name="others"):
    return "bold" in get_attrs(style_name)


def get_border_color():
    return "#aaa"
