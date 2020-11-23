import datetime
import os

import yaml

from meety.config import Config


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
    return datetime.datetime.strptime(text, "%Y-%m-%d")


def str_to_time(text):
    return datetime.datetime.strptime(text, "%H:%M").time()


def str_to_datetime(text):
    return datetime.datetime.strptime(text, "%Y-%m-%d %H:%M")
