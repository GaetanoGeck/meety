"""Meety - quickly start online meetings from YAML."""

import argparse
import os
import shutil
import sys

from meety import args as common_args
from meety import resources
from meety.config import Config
from meety.loader import Loader
from meety.logging import log

PROGRAM = "meety"
VERSION = "0.11.0"
SUMMARY = f"This is {PROGRAM}, version {VERSION}."
URL = "https://github.com/GaetanoGeck/meety/"

DOCUMENTATION_TEMPLATE = """Please edit this file. It contains some comments \
but you can find more information on the web:

  - How to define which meeting specifications are loaded
    https://github.com/GaetanoGeck/meety/blob/main/docs/select-files.md

  - How to specify meetings in YAML
    https://github.com/GaetanoGeck/meety/blob/main/docs/specify-meetings.md
"""


def start_cli():
    try:
        from meety.cli import app
        start_app(app)
    except KeyboardInterrupt:
        print("Goodbye!")


def start_gui():
    from meety.gui import app
    start_app(app)


def start_app(app):
    config = _prepare_config(PROGRAM)
    config.reload()
    args = _prepare_args(app, config)
    _prepare_logger(args)
    log.info(f"command line arguments: {_input_args}")

    if args.init:
        _create_template_meeting_specification(args.init)
        return

    config.apply()
    loader = _load(args)
    app.run(args, loader)


def _prepare_config(program_name):
    Config.PROGRAM = program_name
    config = Config()
    return config


def _prepare_args(app, config):
    argparser = _setup_argparser(app)
    return _combine_args(app, config, argparser)


def _setup_argparser(app):
    argparser = argparse.ArgumentParser(
        prog=sys.argv[0],
        description=__doc__,
        epilog=f"Detailed documentation on {URL}",
    )
    app.add_argparser_arguments(argparser)
    common_args._add_argparser_common_arguments(
        argparser,
        SUMMARY
    )
    return argparser


def _combine_args(app, config, argparser):
    user_args = config.user.args(app.name) or []
    args = user_args + sys.argv[1:]
    global _input_args
    _input_args = args
    return argparser.parse_args(args)


def _prepare_logger(args):
    log.setWarn()
    if args.verbose:
        log.setInfo()
    if args.debug:
        log.setDebug()


def _load(args):
    loader = Loader()
    loader.only_explicit = args.only_explicit
    loader.add_explicit_directories(args.directories)
    loader.add_explicit_files(args.files)
    loader.load()
    return loader


def _create_template_meeting_specification(target):
    source = resources.get_spec_path("example.yaml")
    target = os.path.expanduser(target)
    if os.path.isfile(target):
        log.error(
            f"File '{target}' already exists. "
            "Please remove it first -- if appropriate."
        )
        return
    print(f"Copying meeting specification template to {target}.", end=" ")
    shutil.copy(source, target)
    print("Done.")
    print(DOCUMENTATION_TEMPLATE)


if __name__ == "__main__":
    start_cli()
