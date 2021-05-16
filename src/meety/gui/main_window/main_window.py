from PyQt5.QtCore import (
    QPoint,
    Qt,
    pyqtSignal,
)
from PyQt5.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QWidget,
)

from meety import resources
from meety.gui import static as gui_static
from meety.gui.main_window.meeting_list import Meetings
from meety.gui.main_window.search import SearchWidget
from meety.gui.main_window.status import StatusWidget
from meety.gui.meeting_dialog import MeetingDialog
from meety.io.utils import ensure_between
from meety.logging import log


def url_to_entry(url):
    name = f"URL ({url})"
    return f"- name: {name}\n  url: {url}"


class MainWindow(QWidget):
    query_changed = pyqtSignal(str, name="query_changed")
    rating_mode_toggled = pyqtSignal(bool, name="rating_mode_toggled")
    meeting_chosen = pyqtSignal(object, name="meeting_chosen")
    handler_chosen = pyqtSignal(object, name="handler_chosen")
    reload_requested = pyqtSignal(name="reload_requested")

    def __init__(self, width, height, xpos=0.5, ypos=0.5):
        super().__init__()
        self.resize(width, height)
        self.move(relative_screen_position(xpos, ypos, width, height))
        self._init_style()
        self._add_widgets()
        self._connect_widget_signals()
        self._set_drag_and_drop()

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
        self._meetings = Meetings()
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
        self._meetings.add_meeting_requested.connect(self._on_add_meeting)

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        self.on_key(event)

    def on_key(self, event):
        key = event.key()
        if key == Qt.Key_Down:
            self._meetings.move_selection_down()
        elif key == Qt.Key_Up:
            self._meetings.move_selection_up()
        elif key == Qt.Key_Return:
            self.meeting_chosen.emit(self._meetings.current_meeting)

    def _on_add_meeting(self):
        self.show_add_meeting()

    def show_add_meeting(self, text=""):
        dialog = MeetingDialog(text)
        dialog.exec_()

    def _set_drag_and_drop(self):
        super().setAcceptDrops(True)

    def dragEnterEvent(self, event):
        mime = event.mimeData()
        if mime.hasText() or mime.hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        mime = event.mimeData()
        if mime.hasUrls():
            text = "\n".join(
                [url_to_entry(u) for u in mime.urls()]
            )
        elif mime.hasText():
            text = mime.text()
        else:
            log.warning("Unknown MIME content dropped.")
            return
        self.show_add_meeting(text)

    def update_rated_meetings(self, rated_meetings):
        self._meetings.update_rated_meetings(rated_meetings)

    def set_meetings_name(self, name):
        self._meetings.set_name(name)

    def notify_quickly(self, text):
        self._status.notify_quickly(text)

    def notify(self, text, tooltip=""):
        self._status.notify(text, tooltip)

    def warn(self, text, tooltip=""):
        self._status.warn(text, tooltip)

    def clear_notifications(self):
        self._status.clear_notifications()


def relative_screen_position(rel_xpos, rel_ypos, width, height):
    screen = QApplication.desktop().screenGeometry()
    screen.adjust(0, 0, -width, -height)
    rel_xpos = ensure_between(
        value=rel_xpos,
        at_least=0.0,
        at_most=1.0,
        on_wrong_type=0.5
    )
    rel_ypos = ensure_between(
        value=rel_ypos,
        at_least=0.0,
        at_most=1.0,
        on_wrong_type=0.5
    )
    return QPoint(
        rel_xpos * screen.width(),
        rel_ypos * screen.height()
    )
