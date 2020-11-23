import importlib.resources as resources

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (
    QVBoxLayout,
    QWidget,
)

from meety.gui import static as gui_static
from meety.gui.main_window.meeting_list import MeetingList
from meety.gui.main_window.search import SearchWidget
from meety.gui.main_window.status import StatusWidget


class MainWindow(QWidget):
    query_changed = pyqtSignal(str, name="query_changed")
    rating_mode_toggled = pyqtSignal(bool, name="rating_mode_toggled")
    meeting_chosen = pyqtSignal(object, name="meeting_chosen")
    handler_chosen = pyqtSignal(object, name="handler_chosen")
    reload_requested = pyqtSignal(name="reload_requested")

    def __init__(self, width, height):
        super().__init__()
        self.resize(width, height)
        self._init_style()
        self._add_widgets()
        self._connect_widget_signals()

    def _init_style(self):
        with resources.open_text(gui_static, "stylesheet.css") as css:
            self.setStyleSheet(css.read())

    def _add_widgets(self):
        layout = self._create_layout()
        layout.addWidget(self._create_search())
        layout.addWidget(self._create_meetings())
        layout.addWidget(self._create_status())
        self.setLayout(layout)

    def _create_layout(self):
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        return layout

    def _create_search(self):
        self._search = SearchWidget()
        return self._search

    def _create_meetings(self):
        self._meetings = MeetingList()
        return self._meetings

    def _create_status(self):
        self._status = StatusWidget()
        return self._status

    def _connect_widget_signals(self):
        self._search.textChanged.connect(self.query_changed.emit)
        self._meetings.rating_mode_toggled.connect(
            self.rating_mode_toggled.emit
        )
        self._meetings.handler_chosen.connect(self.handler_chosen.emit)
        self._meetings.meeting_chosen.connect(self.meeting_chosen.emit)
        self._meetings.reload_requested.connect(self.reload_requested.emit)

    def update_rated_meetings(self, rated_meetings):
        self._meetings.update_rated_meetings(rated_meetings)

    def set_meetings_name(self, name):
        self._meetings.set_name(name)

    def notify_quickly(self, text):
        self._status.notify_quickly(text)

    def notify(self, text, tooltip=""):
        self._status.notify(text, tooltip)
        self._status.setToolTip(tooltip)

    def clear_notifications(self):
        self._status.clear_notifications()
