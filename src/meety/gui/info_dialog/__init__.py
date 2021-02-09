from PyQt5.QtWidgets import (
    QDialog,
    QTabWidget,
    QVBoxLayout,
)

from meety.gui.info_dialog.about import TabAbout
from meety.gui.info_dialog.files import TabFiles
from meety.gui.info_dialog.log import TabLog
from meety.gui.info_dialog.meetings import TabMeetings
from meety.gui.info_dialog.system import TabSystem


class InfoDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Info")
        self._init_style()
        self._add_widgets()
        self._connect_widget_signals()

    def _init_style(self):
        pass

    def _add_widgets(self):
        layout = QVBoxLayout()
        tabs = QTabWidget()
        tabs.setContentsMargins(0, 0, 0, 0)
        tabs.addTab(TabAbout(), "&About")
        tabs.addTab(TabSystem(), "&System")
        tabs.addTab(TabFiles(), "&Files")
        tabs.addTab(TabMeetings(), "&Meetings")
        tabs.addTab(TabLog(), "&Log")
        layout.addWidget(tabs)
        self.setLayout(layout)

    def _connect_widget_signals(self):
        pass
