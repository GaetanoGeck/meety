from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (
    QCheckBox,
    QHBoxLayout,
    QWidget,
)


class OptionsWidget(QWidget):
    rating_mode_toggled = pyqtSignal(bool, name="ratingModeToggled")

    def __init__(self):
        super().__init__()
        self._init_style()
        self._add_widgets()
        self._connect_widget_signals()

    def _init_style(self):
        pass

    def _add_widgets(self):
        layout = self._create_layout()
        layout.addStretch(1)
        layout.addWidget(self._create_rating_mode())
        self.setLayout(layout)

    def _create_layout(self):
        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        return layout

    def _create_rating_mode(self):
        self._rating_mode = QCheckBox("only &matching")
        self._rating_mode.setToolTip(" ".join([
            "Show only meetings with matching time or",
            "query constraints. Hide others.",
        ]))
        return self._rating_mode

    def _connect_widget_signals(self):
        self._rating_mode.toggled.connect(self.rating_mode_toggled.emit)
