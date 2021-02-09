"""Windows implementation for system-dependent functionality."""

import os
import subprocess

icon_resolution = 256
icon_extension = "ico"
icon_path = None
desktop_extension = None
desktop_path = None
executable = "meety.exe"


def frozen_script_and_executable(path):
    path_to_exe = os.path.join(path, executable)
    return {
        # This is a hack to allow to create a shortcut
        # to an executable via `pyshortcuts`
        "executable": f"%%comspec /K start '' '{path_to_exe}' & exit & rem",
        "script": "src/gui.py",
    }


def is_installed(app):
    """Determine whether program `app` can be found."""
    result = subprocess.run(
        ['where', app],
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def update_shortcut_database():
    pass
