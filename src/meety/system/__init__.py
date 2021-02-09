"""System-dependent functionality."""

import os
import pathlib
import platform
import shutil
import sys

from meety import resources
from meety.logging import log

DESCRIPTION = """Meety - quickly start online meetings from YAML."""

SYSTEM = platform.system()
_running = None
log.debug(f"Your system is '{SYSTEM}'")
if SYSTEM == "Linux":
    from meety.system import linux
    _running = linux
elif SYSTEM == "Darwin":
    from meety.system import darwin
    _running = darwin
elif SYSTEM == "Windows":
    from meety.system import windows
    _running = windows
else:
    log.warning(f"System '{SYSTEM}' is unknown.")


def icon_resolution():
    return _running.icon_resolution


def icon_extension():
    return _running.icon_extension


def desktop_extension():
    return _running.desktop_extension


def desktop_path(filename):
    return os.path.join(_running.desktop_path, filename)


def icon_path(filename):
    return os.path.join(_running.icon_path, filename)


def executable():
    return _running.executable


def satisfies(system, installed):
    """Tests whether the app runs on the given system and whether the
    given program is installed."""
    return all([
        not system or SYSTEM.lower() == system.lower(),
        not installed or _running.is_installed(installed),
    ])


def create_shortcut(desktop=True, startmenu=True):
    filename = f"meety-{icon_resolution()}.{icon_extension()}"
    icon_path = resources.get_icon_path(filename)
    log.debug(f"Creating shortcut with icon '{icon_path}'.")

    try:
        msg = create_shortcut_via_pyshortcuts(icon_path, desktop, startmenu)
    except ImportError:
        log.warning("Module 'pyshortcuts' is not available!")
        msg = try_to_copy_desktop_file(filename)

    if msg is True:
        _running.update_shortcut_database()
    return msg


def create_shortcut_via_pyshortcuts(icon_path, desktop=True, startmenu=True):
    from pyshortcuts import make_shortcut

    target = script_and_executable()
    if target is None:
        log.error("Script/executable is not defined. Cannot create shortcut.")
        return False
    else:
        log.debug(f"Script/executable = '{target}'")
    make_shortcut(
        **target,
        name="Meety",
        description=DESCRIPTION,
        icon=icon_path,
        terminal=False,
        desktop=desktop,
        startmenu=startmenu,
    )
    return True


def try_to_copy_desktop_file(filename):
    log.info("Try to copy desktop/icon file.")
    try:
        copy_desktop_file()
        copy_icon(filename)
    except Exception as e:
        return str(e)
    else:
        return True


def copy_desktop_file():
    filename = f"meety.{desktop_extension()}"
    source = resources.get_desktop_path(filename)
    target = desktop_path(filename)
    shutil.copy(source, target)


def copy_icon(filename):
    source = resources.get_icon_path(filename)
    target = icon_path(filename)
    shutil.copy(source, target)


def script_and_executable():
    if getattr(sys, "frozen", False):
        log.debug("Application is 'frozen'.")
        raise Exception(
            "Shortcut creation for application bundles is not yet supported. "
            "Sorry!"
        )
        # TODO: Support application bundles
        # path = sys._MEIPASS
        # return _running.frozen_script_and_executable(path)
    else:
        log.debug("Application is _not_ 'frozen'.")
        system_path = os.path.dirname(os.path.abspath(__file__))
        path = pathlib.Path(system_path)
        base_path = path.parent.parent
        return {
            "script": os.path.join(base_path, "gui.py")
        }
