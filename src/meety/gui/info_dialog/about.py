from PyQt5 import QtCore
from PyQt5.QtWidgets import QLabel

from meety.__main__ import (
    SUMMARY,
    URL,
)

ABOUT = f"""<b>Meety - quickly start online meetings from YAML</b><br/>
{SUMMARY}<br/>
<br/>
<a href="{URL}">{URL}</a><br/>
<br/>
Copyright The Contributors to the <i>Meety</i> project.
"""


class TabAbout(QLabel):
    def __init__(self):
        super().__init__()
        self._init_style()
        self._add_widgets()
        self._connect_widget_signals()

    def _init_style(self):
        pass

    def _add_widgets(self):
        self.setText(ABOUT)
        self.setMargin(10)
        self.setAlignment(QtCore.Qt.AlignTop)
        self.setOpenExternalLinks(True)

    def _connect_widget_signals(self):
        pass
