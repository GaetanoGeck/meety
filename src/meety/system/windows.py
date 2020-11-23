"""Windows implementation for system-dependent functionality."""

import subprocess


def is_installed(app):
    """Determine whether program `app` can be found."""
    result = subprocess.run(
        ['where', app],
        capture_output=True,
        text=True,
    )
    return result.returncode == 0
