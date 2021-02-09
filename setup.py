import os
import re

from setuptools import setup
from setuptools.config import read_configuration

with open("src/meety/__main__.py", encoding="utf8") as f:
    version = re.search(r'VERSION = "(.*?)"', f.read()).group(1)

config_file = os.path.join(os.path.dirname(__file__), "setup.cfg")
config = read_configuration(config_file)

setup(
    **config["metadata"],
    **config["options"],
    package_data={
        "meety": [
            os.path.join("static", "config", "*.yaml"),
            os.path.join("static", "icons", "*.png"),
            os.path.join("static", "spec", "*.yaml"),
            os.path.join("gui", "static", "*.css"),
        ]
    },
    version=version,
)
