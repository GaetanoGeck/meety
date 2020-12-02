"""Meety - quickly connect to online meetings managed in YAML."""

import argparse
import sys

from meety import args as common_args
from meety.config import Config
from meety.loader import Loader
from meety.logging import log

PROGRAM = "meety"
VERSION = "0.9.2"
SUMMARY = f"This is {PROGRAM}, version {VERSION}."
URL = "https://github.com/GaetanoGeck/meety/"


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


if __name__ == "__main__":
    start_cli()
