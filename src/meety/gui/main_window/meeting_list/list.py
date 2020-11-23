from PyQt5.QtCore import (
    QEvent,
    Qt,
    pyqtSignal,
)
from PyQt5.QtWidgets import (
    QGridLayout,
    QLabel,
    QListWidget,
    QWidget,
)

from meety.gui.main_window.meeting_list.context import MeetingItemMenu
from meety.gui.main_window.meeting_list.delegate import ItemDelegate
from meety.gui.main_window.meeting_list.item import MeetingItem
from meety.gui.main_window.options import OptionsWidget


class MeetingList(QWidget):
    meeting_chosen = pyqtSignal(object, name="meeting_chosen")
    handler_chosen = pyqtSignal(object, name="handler_chhosen")
    reload_requested = pyqtSignal(name="reload_requested")
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
        self._list = QListWidget()
        item_delegate = ItemDelegate()
        self._list.setItemDelegate(item_delegate)
        return self._list

    def _connect_widget_signals(self):
        self._list.itemActivated.connect(self._choose_meeting)
        self._options.rating_mode_toggled.connect(
            self.rating_mode_toggled.emit
        )
        self._list.installEventFilter(self)

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

    def _choose_meeting(self, item):
        rmeeting = item.data(Qt.UserRole)
        self.meeting_chosen.emit(rmeeting.meeting)

    def eventFilter(self, source, event):
        if event.type() == QEvent.ContextMenu and source is self._list:
            return self._context_menu_on_list(source, event)
        return super().eventFilter(source, event)

    def _context_menu_on_list(self, source, event):
        item = source.itemAt(event.pos())
        rmeeting = item.data(Qt.UserRole)
        menu = MeetingItemMenu(rmeeting.meeting)
        menu.handler_chosen.connect(self.handler_chosen.emit)
        menu.reload_requested.connect(self.reload_requested.emit)
        menu.exec_(event.globalPos())
        return True
