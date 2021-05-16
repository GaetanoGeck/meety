"""The graphical user interface program."""

import signal

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication

from meety import connect
from meety.__main__ import PROGRAM
from meety.gui.args import add_argparser_arguments  # USED
from meety.gui.icons import get_icon
from meety.gui.main_window import MainWindow
from meety.io import copy_to_clipboard
from meety.logging import log
from meety.meetings.rating import Ratings

name = "gui"
last_query = []
matching_only = False


def run(args, loader):
    global _loader
    _loader = loader

    _save_args(args)
    _save_meetings(loader.meetings)
    _update_meetings()

    app = _create_app()
    _create_window()
    _on_query_changed("")

    _setup_interrupt_handling()
    window.show()
    app.exec_()


def _save_args(args):
    global _args
    _args = args


def _save_meetings(meetings):
    global _all_meetings
    _all_meetings = meetings


def get_all_meetings():
    return _all_meetings


def get_loaded_paths():
    return _loader.loaded_paths


def get_active_directories():
    return _loader.active_directories


def _create_app():
    app = QApplication([])
    icon = get_icon(PROGRAM)
    app.setApplicationName(PROGRAM)
    app.setApplicationDisplayName(PROGRAM)
    app.setWindowIcon(icon)
    return app


def _create_window():
    global window
    window = MainWindow(
        width=_args.window_width,
        height=_args.window_height,
        xpos=_args.window_xpos,
        ypos=_args.window_ypos
    )
    _connect_signals()
    _warn_on_loading_failures()


def _update_meetings():
    global rating
    rating = Ratings(_all_meetings)


def _connect_signals():
    window.query_changed.connect(_on_query_changed)
    window.rating_mode_toggled.connect(_on_rating_mode_toggled)
    window.meeting_chosen.connect(_on_meeting_chosen)
    window.handler_chosen.connect(_on_handler_chosen)
    window.reload_requested.connect(_on_reload_requested)

    global timer
    timer = QTimer()
    timer.timeout.connect(_on_time_changed)
    timer.start(1000)


def _warn_on_loading_failures():
    failures = _loader.loaded_paths.all_failures
    if failures:
        text = (
            f"Failed to load {len(failures)} file(s): "
            + ",".join(failures),
        )
        tooltip = "\n".join(f"- {f}" for f in failures)
        window.warn(text, tooltip)


def add_meeting_file(filename):
    _loader.add_file(filename)
    _on_reload_requested()


def add_meeting_specs(text):
    _loader.add_runtime_specs(text)
    _on_reload_requested()


def _on_reload_requested():
    _loader.reload()
    window.notify("Reloaded meetings.")
    global _all_meetings
    _all_meetings = _loader.meetings
    _update_meetings()


def _on_time_changed():
    _update_rated_meetings()


def _on_query_changed(text):
    global last_query
    last_query = text.split(" ")
    _update_rated_meetings()


def _on_rating_mode_toggled(status):
    global matching_only
    matching_only = status
    global window
    window.set_meetings_name({
        False: "All meetings",
        True: "Matching meetings",
    }[status])
    _update_rated_meetings()


def _on_meeting_chosen(meeting):
    window.clear_notifications()
    if _args.copy_password:
        _copy_password(meeting)
    handler = _get_handler(meeting)
    _on_handler_chosen((handler, meeting))


def _on_handler_chosen(handler_meeting_pair):
    handler, meeting = handler_meeting_pair
    if handler:
        connect_with_handler(handler, meeting)
    else:
        window.notify("Sorry, no connection handler found!")


def _update_rated_meetings():
    rated_meetings = _rate()
    window.update_rated_meetings(rated_meetings)


def _rate():
    rating.rate(last_query)
    if matching_only:
        return rating.get_all_matching()
    else:
        return rating.get_all()


def _copy_password(meeting):
    password = meeting.data.get("password")
    if password:
        window.notify_quickly("...Copied password to clipboard.")
        copy_to_clipboard(password)


def _get_handler(meeting):
    handlers = connect.applicable_handlers(meeting)
    log.debug(f"Handlers found: {handlers}")
    if not handlers:
        return None
    handler = handlers[0]
    log.debug(f"Handler chosen: {handler}")
    return handler


def connect_with_handler(handler, meeting):
    error = connect.start(handler)
    if error:
        window.notify(error)
    else:
        msg = " ".join([
            f"Started meeting <i>{meeting.name}</i>",
            f"with handler <i>{handler.name}</i>.",
        ])
        window.notify(msg, handler.cmd)


def _setup_interrupt_handling():
    signal.signal(signal.SIGINT, _interrupt_handler)


def _interrupt_handler(signum, frame):
    print("Goodbye!")
    QApplication.quit()
