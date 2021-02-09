"""Linux implementation for system-dependent functionality."""

import os
import subprocess

icon_resolution = 256
icon_extension = "png"
icon_path = os.path.expanduser("~/.icons")
desktop_extension = "desktop"
desktop_path = os.path.expanduser("~/.local/share/applications")
executable = "meety"
frozen_script_and_executable = None


def is_installed(app):
    """Determine whether program `app` can be found."""
    result = subprocess.run(
        ['which', app],
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def update_shortcut_database():
    subprocess.run(["update-desktop-database"])
