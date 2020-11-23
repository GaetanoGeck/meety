import subprocess

from meety.connect import handlers as connect_handlers
from meety.logging import log

handlers = connect_handlers.Handlers()


def set_options(config):
    """Set options for module `connect`."""
    if isinstance(config, dict):
        connect_handlers.set_options(
            handlers,
            config.get("handlers") or []
        )
    else:
        log.expected("dictionary", "connect", config)


def start(handler, test_run=False):
    """Start a meeting by running the provided command."""
    if test_run:
        return ""
    try:
        log.info(f"Run '{handler.cmd}' with options '{handler.options}'")
        subprocess.Popen(handler.cmd.split(" "), **handler.options)
        log.info("... successful.")
    except FileNotFoundError:
        log.info("... failed.")
        error = f"Failed to execute handler '{handler.cmd}'!"
        log.error(error)
        return error
    else:
        return ""


def applicable_handlers(meeting):
    """Return a list of all applicable handlers, ordered by preference."""
    return list(generate_applicable_handlers(meeting))


def generate_applicable_handlers(meeting):
    """Return a generator for all applicable handlers,
    ordered by preference.
    """
    for handler in handlers.ordered:
        cmd, options = try_handler(handler, meeting)
        if cmd:
            yield connect_handlers.NamedHandler(
                handler.name,
                cmd,
                options
            )


def try_handler(handler, meeting):
    """Try to apply a handler based on the meeting's data.
    Returns the resulting command on success and `None` otherwise.
    """
    log.debug(f"Try handler '{handler.name}'.")
    try:
        cmd = handler.cmd.format_map(meeting.data)
    except KeyError:
        log.debug(f"Handler '{handler.name}' misses information.")
        return (None, None)
    else:
        return (cmd, handler.options)
