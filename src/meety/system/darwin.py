"""MacOS implementation for system-dependent functionality."""

import subprocess

icon_resolution = 256
icon_extension = "icns"
icon_path = None
desktop_extension = None
desktop_path = None
executable = "meety"
frozen_script_and_executable = None


def is_installed(app):
    """Determine whether program `app` can be found."""
    result = subprocess.run(
        [
            "mdfind",
            "-count",
            f"kMDItemFSName == {app}"
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode > 0 or result.stderr:
        return False
    elif int(result.stdout) >= 1:
        return True


def update_shortcut_database():
    pass
