"""MacOS implementation for system-dependent functionality."""

import subprocess


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
