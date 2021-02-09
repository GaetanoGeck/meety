import datetime
import os

import yaml

from meety.config import Config
from meety.meetings.preferences import TimeMatchDescription


def testpath(path):
    return os.path.join("test", *path)


def load(path):
    path = testpath(path)
    with open(path) as yamlFile:
        return yaml.load(yamlFile, Loader=yaml.BaseLoader)


def apply_language_configurations(*langs):
    config = Config()
    for lang in langs:
        config._load_additional_config(lang)
    for ac in config.additional_configs:
        ac.apply()


def str_to_date(text):
    if text is None:
        return None
    return datetime.datetime.strptime(text, "%Y-%m-%d")


def str_to_time(text):
    if text is None:
        return None
    return datetime.datetime.strptime(text, "%H:%M").time()


def str_to_datetime(text):
    if text is None:
        return None
    return datetime.datetime.strptime(text, "%Y-%m-%d %H:%M")


def md2bool(match_description):
    """Convert matching to `True`, others to `False`."""
    return match_description != TimeMatchDescription.NOT_MATCHING
