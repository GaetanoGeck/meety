"""System-dependent functionality."""

import platform

from meety.logging import log

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


def satisfies(system, installed):
    """Tests whether the app runs on the given system and whether the
    given program is installed."""
    return all([
        not system or SYSTEM.lower() == system.lower(),
        not installed or _running.is_installed(installed),
    ])
