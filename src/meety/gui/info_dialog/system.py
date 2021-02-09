from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QCheckBox,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from meety.system import create_shortcut

EXPLANATION = """<b>Create shortcuts to <i>Meety</i> (GUI application).</b>
<br/><br/>
Whether shortcuts are added to your desktop and/or your
startmenu depends on your choice below <i>and on your system</i>.
"""


class TabSystem(QWidget):
    def __init__(self):
        super().__init__()
        self._init_style()
        self._add_widgets()
        self._connect_widget_signals()

    def _init_style(self):
        pass

    def _add_widgets(self):
        layout = QVBoxLayout()
        layout.setSpacing(3)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.addWidget(self._create_explanation())
        layout.addWidget(self._create_desktop_option())
        layout.addWidget(self._create_startmenu_option())
        layout.addWidget(self._create_shortcut_button())
        layout.addStretch(1)
        self.setLayout(layout)

    def _create_explanation(self):
        self._explanation = QLabel(EXPLANATION)
        self._explanation.setWordWrap(True)
        self._explanation.setAlignment(QtCore.Qt.AlignTop)
        return self._explanation

    def _create_desktop_option(self):
        self._desktop_option = QCheckBox("on &desktop")
        self._desktop_option.setChecked(True)
        return self._desktop_option

    def _create_startmenu_option(self):
        self._startmenu_option = QCheckBox("on &startmenu")
        self._startmenu_option.setChecked(True)
        return self._startmenu_option

    def _create_shortcut_button(self):
        self._shortcut_button = QPushButton("&create")
        return self._shortcut_button

    def _connect_widget_signals(self):
        self._shortcut_button.clicked.connect(self._create_shortcut)

    def _create_shortcut(self):
        desktop = self._desktop_option.isChecked()
        startmenu = self._startmenu_option.isChecked()
        msg = QMessageBox()
        try:
            result = create_shortcut(desktop, startmenu)
        except Exception as e:
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Error on shortcut creation.")
            msg.setDetailedText(str(e))
        else:
            if result is True:
                msg.setIcon(QMessageBox.Information)
                msg.setText("Shortcut(s) created.")
            else:
                msg.setIcon(QMessageBox.Warning)
                msg.setText(f"Shortcut(s) <i>not</i> created: {result}")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
