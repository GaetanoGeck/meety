"""Meetings and ratings, time preferences of/for them."""

from meety import io
from meety.meetings import preferences


def reset_options():
    io.reset_options()
    preferences.reset_options()


def set_options(config, name):
    io.set_options(config, name)
    preferences.set_options(config.get("preferences") or {}, name)
