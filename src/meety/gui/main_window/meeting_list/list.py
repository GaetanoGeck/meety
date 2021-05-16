import time

from PyQt5.QtCore import (
    QEvent,
    QMimeData,
    Qt,
    pyqtSignal,
)
from PyQt5.QtGui import (
    QDrag,
    QKeySequence,
)
from PyQt5.QtWidgets import (
    QApplication,
    QGridLayout,
    QLabel,
    QListWidget,
    QWidget,
)

from meety import io
from meety.gui.info_dialog.files import TabFiles
from meety.gui.main_window.meeting_list.context import MeetingItemMenu
from meety.gui.main_window.meeting_list.delegate import ItemDelegate
from meety.gui.main_window.meeting_list.item import MeetingItem
from meety.gui.main_window.options import OptionsWidget


class Meetings(QWidget):
    meeting_chosen = pyqtSignal(object, name="meeting_chosen")
    handler_chosen = pyqtSignal(object, name="handler_chosen")
    reload_requested = pyqtSignal(name="reload_requested")
    add_meeting_requested = pyqtSignal(name="add_meeting_requested")
    rating_mode_toggled = pyqtSignal(bool, name="rating_mode_toggled")

    def __init__(self):
        super().__init__()
        self.name = "Meetings"
        self._init_style()
        self._add_widgets()
        self._connect_widget_signals()
        self.update_rated_meetings([])

    def _init_style(self):
        pass

    def _add_widgets(self):
        layout = self._create_layout()
        layout.addWidget(self._create_info(), 0, 0)
        layout.addWidget(self._create_options(), 0, 1)
        layout.addWidget(self._create_list(), 1, 0, 1, 2)
        layout.addWidget(self._create_file_status(), 2, 0, 1, 2)
        self.setLayout(layout)

    def _create_layout(self):
        layout = QGridLayout()
        layout.setRowStretch(0, 0)
        layout.setRowStretch(1, 1)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        return layout

    def _create_info(self):
        self._info = QLabel("Meetings")
        self._info.setStyleSheet("""
            font: bold;
            margin-top: 5px;
        """)
        return self._info

    def _create_options(self):
        self._options = OptionsWidget()
        return self._options

    def _create_list(self):
        self._list = MeetingList()
        return self._list

    def _create_file_status(self):
        self._file_status = TabFiles()
        return self._file_status

    def _connect_widget_signals(self):
        self._list.itemActivated.connect(self._choose_meeting)
        self._options.rating_mode_toggled.connect(
            self.rating_mode_toggled.emit
        )
        self._list.installEventFilter(self)
        delegate = self._list.get_item_delegate()
        delegate.context_menu_requested.connect(
            self._context_menu_from_delegate
        )

    @property
    def current_meeting(self):
        return self._list.current_meeting

    def set_name(self, name):
        self.name = name
        self._update_info()

    def update_rated_meetings(self, rated_meetings):
        self._rated_meetings = rated_meetings
        self._update_info()
        self._update_entries(rated_meetings)

    def _update_info(self):
        num = len(self._rated_meetings)
        self._info.setText(f"{self.name} ({num})")

    def _update_entries(self, rated_meetings):
        row = self._list.currentRow()
        last = len(rated_meetings) - 1
        self._list.clear()
        for rmeeting in rated_meetings:
            item = MeetingItem(rmeeting)
            self._list.addItem(item)
        self._list.setCurrentRow(min(row, last))
        if rated_meetings:
            self._file_status.hide()

    def _choose_meeting(self, item):
        rmeeting = item.data(Qt.UserRole)
        self.meeting_chosen.emit(rmeeting.meeting)

    def eventFilter(self, source, event):
        if event.type() == QEvent.ContextMenu and source is self._list:
            return self._context_menu_on_list(source, event)
        return super().eventFilter(source, event)

    def _context_menu_from_delegate(self, event):
        return self._context_menu_on_list(self._list, event)

    def _context_menu_on_list(self, source, event):
        item = source.itemAt(event.pos())
        meeting = None
        if item:
            meeting = item.data(Qt.UserRole).meeting
        menu = MeetingItemMenu(meeting)
        menu.handler_chosen.connect(self.handler_chosen.emit)
        menu.reload_requested.connect(self.reload_requested.emit)
        menu.add_meeting_requested.connect(self.add_meeting_requested.emit)
        menu.exec_(event.globalPos())
        return True

    def move_selection_down(self):
        self._list.move_selection_down()

    def move_selection_up(self):
        self._list.move_selection_up()


class MeetingList(QListWidget):
    COPY_COMPLETE_TIMESPAN = 2000

    def __init__(self):
        super().__init__()
        self.setProperty("class", "meetings")
        self._set_delegate()
        self._set_drag_and_drop()
        self._copy_tracker = EventTimingTracker(self.COPY_COMPLETE_TIMESPAN)
        self.setCurrentRow(0)

    def get_item_delegate(self):
        return self._item_delegate

    def _set_delegate(self):
        self._item_delegate = ItemDelegate()
        super().setItemDelegate(self._item_delegate)
        self._item_delegate.setParent(self)

    def move_selection_down(self):
        self.move_selection_by(+1)

    def move_selection_up(self):
        self.move_selection_by(-1)

    def move_selection_by(self, offset):
        self.move_selection_to(self.currentRow() + offset)

    def move_selection_to(self, row):
        new_row = self._valid_selection(row)
        if new_row is not None:
            super().setCurrentRow(new_row)

    def _valid_selection(self, row):
        start_selection = 0 if self.count() > 0 else None
        return io.utils.ensure_between(
            value=row,
            at_least=0,
            at_most=super().count()-1,
            on_wrong_type=start_selection
        )

    def _set_drag_and_drop(self):
        super().setDragEnabled(True)

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        if event.matches(QKeySequence.Copy):
            close_to_last_copy = self._copy_tracker.new_event()
            self._copy_to_clipboard(complete=close_to_last_copy)

    def _copy_to_clipboard(self, complete):
        mime_data = self._get_mime_data(complete)
        QApplication.clipboard().setMimeData(mime_data)

    def mouseMoveEvent(self, event):
        drag = QDrag(self)
        complete = event.modifiers() & Qt.ShiftModifier
        drag.setMimeData(self._get_mime_data(complete))
        drag.exec_(Qt.MoveAction)

    def _get_mime_data(self, complete):
        mime_data = QMimeData()
        if complete:
            self._set_mime_data_complete(mime_data)
        else:
            self._set_mime_data_minimal(mime_data)
        return mime_data

    def _set_mime_data_complete(self, mime_data):
        meeting = self.current_meeting
        mime_data.setText(meeting.input_data_to_str())

    def _set_mime_data_minimal(self, mime_data):
        meeting = self.current_meeting
        urls = meeting.urls
        if len(urls) == 0:
            url_text = "<NO URLs>"
        elif len(urls) == 1:
            url_text = urls[0]
        else:
            url_text = "\n" + "\n".join([f"- {u}" for u in urls])
        mime_data.setText(f"{meeting.name}: {url_text}")

    @property
    def current_meeting(self):
        return self.currentItem().data(Qt.UserRole).meeting


class EventTimingTracker:
    """Register new events and check whether the last event happened
    within the given time span."""

    def __init__(self, time_span):
        self._last = 0
        self._time_span = time_span

    """Returns True if and only if the new event is close to the last."""

    def new_event(self):
        current = time.time() * 1000
        close = current - self._last < self._time_span
        self._last = current
        return close
