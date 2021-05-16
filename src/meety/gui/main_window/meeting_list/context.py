from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMenu

from meety import connect
from meety.io import copy_to_clipboard


class MeetingItemMenu(QMenu):
    handler_chosen = pyqtSignal(object, name="handler_chosen")
    reload_requested = pyqtSignal(name="reload_requested")
    add_meeting_requested = pyqtSignal(name="add_meeting_requested")

    def __init__(self, meeting):
        super().__init__()
        self._meeting = meeting
        self._counter = 0
        self._add_actions()

    def _add_actions(self):
        self._actions = {}
        if self._meeting:
            self.addAction("Copy &input data", self._on_copy_input)
            self.addAction("Copy &derived data", self._on_copy_derived)
            self._add_handler_actions()
            self.addSeparator()
        self.addAction("&Reload all meetings", self._on_reload)
        self.addAction("&Add meeting", self._on_add_meeting)

    def _add_handler_actions(self):
        if self._meeting is None:
            return
        handlers = connect.applicable_handlers(self._meeting)
        if len(handlers) > 0:
            self.addSeparator()
        for handler in handlers:
            self._add_handler_action(handler)

    def _add_handler_action(self, handler):
        self._counter += 1
        number = str(self._counter)
        if self._counter < 10:
            # add shortcut for first entries,
            # distinguishable by the first digit
            number = "&" + number
        self.addAction(
            f"{number}. Connect via {handler.name}",
            lambda: self._on_handler(handler)
        )

    def _on_copy_input(self):
        text = self._meeting.input_data_to_str()
        copy_to_clipboard(text)

    def _on_copy_derived(self):
        text = self._meeting.data_to_str()
        copy_to_clipboard(text)

    def _on_handler(self, handler):
        self.handler_chosen.emit((handler, self._meeting))

    def _on_reload(self):
        self.reload_requested.emit()

    def _on_add_meeting(self):
        self.add_meeting_requested.emit()
