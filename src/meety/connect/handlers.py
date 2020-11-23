import fnmatch
from collections import namedtuple

from meety import (
    io,
    system,
)
from meety.logging import log

NamedHandler = namedtuple("NamedHandler", "name cmd options")


def set_options(handlers, actions):
    if not isinstance(actions, list):
        log.expected("list", "connection handlers", actions)
        return

    for entry in actions:
        if isinstance(entry, dict):
            handlers.apply_action(entry)
        else:
            log.expected(
                "dictionary",
                "connection handler",
                entry
            )


class Handlers:
    """An ordered list of handlers.

    Handlers have a name (for reference) and a command. They are
    ordered linearly by preference. The preference order can be
    changed by the user: handlers can be removed, prepended and
    appended. New handlers can be registered as well.

    Changing of the preference is independent from the registration
    of a command for a handler. The intention behind this is that
    handlers should ideally be provided by the application while
    their preferred order is more subjective.
    """

    def __init__(self):
        """At the beginning, no handler is registered."""
        self._command = {}
        self._order = []

    def register(self, entry):
        """Register handler with a name and a command in `entry`."""
        name = entry["name"]
        cmd = entry["command"]
        options = {}
        options["shell"] = io.str_is_true(entry.get("shell", "False"))
        req_system = entry.get("system")
        req_app = entry.get("installed")
        if system.satisfies(req_system, req_app):
            self._command[name] = (cmd, options)
            self.append(entry)

    @property
    def ordered(self):
        """Yield all handlers with a command, ordered by preference."""
        for name in self._order:
            cmd, options = self._command.get(name)
            if cmd:
                yield NamedHandler(name, cmd, options)

    def prepend(self, entry):
        """Add handler with name in `entry` as the first handler.
        If the handler already occurs in the preference order, then
        the latter occurrence is removed.
        """
        name = entry["name"]
        self.remove(entry, True)
        self._order.insert(0, name)

    def append(self, entry):
        """Add handler with name in `entry`as the last handler.
        If the handler already occurs in the preference order, then
        it is not added. If you want to move to the end, remove it
        first.
        """
        name = entry["name"]
        if name not in self._order:
            self._order.append(name)

    def remove(self, entry, silent=False):
        """Remove all handlers with names matching the name in `entry`.
        If `silent` is `True`, then it will be logged if there is
        handler with a matching name.
        """
        name = entry["name"]
        matches = fnmatch.filter(self._order, name)
        for name in matches:
            log.debug(f"Remove handler '{name}'.")
            self._order.remove(name)
        if not matches and not silent:
            log.debug(f"No handler matches pattern '{name}'.")

    def apply_action(self, entry):
        """Try to apply action and log errors."""
        call = self._determine_action(entry)
        try:
            call(entry)
        except KeyError as e:
            log.warning(
                f"Failed to apply action '{entry}',"
                f" missing attribute {e}."
            )
        except Exception as e:
            log.warning(f"Failed to apply action '{entry}'.")
            log.exception(e)

    def _determine_action(self, entry):
        """Call the action defined by 'action' attribute."""
        action = entry.get("action")
        if not action:
            log.expected("attribute 'action'", "action", entry)
            return

        call = {
            "register": self.register,
            "prepend": self.prepend,
            "append": self.append,
            "remove": self.remove,
        }.get(action)
        return call

    def __str__(self):
        """List all handler definitions and the order of handlers."""
        return "\n".join([
            self._info_definitions(),
            "",
            self._info_order(),
        ])

    def _info_definitions(self):
        """Return string that lists all defined handlers (name: command)."""
        defs = len(self._command)
        info = [f"Handler definitions ({defs}):"]
        for (name, (cmd, options)) in self._command.items():
            if options == {}:
                opt_info = "no options"
            else:
                opt_info = ", ".join([
                    f"{k}={v}"
                    for (k, v) in options.items()
                ])
            info.append(f"  - {name}: {cmd} ({opt_info})")
        return "\n".join(info)

    def _info_order(self):
        """Return string that lists all handlers according to their order."""
        ords = len(self._order)
        info = [f"Order definitions ({ords}):"]
        for name in self._order:
            info.append(f"  - {name}")
        return "\n".join(info)
