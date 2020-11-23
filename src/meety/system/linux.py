"""Linux implementation for system-dependent functionality."""

import subprocess


def is_installed(app):
    """Determine whether program `app` can be found."""
    result = subprocess.run(
        ['which', app],
        capture_output=True,
        text=True,
    )
    return result.returncode == 0
