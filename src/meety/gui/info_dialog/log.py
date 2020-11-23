from PyQt5.QtWidgets import (
    QComboBox,
    QPlainTextEdit,
    QVBoxLayout,
    QWidget,
)

from meety.logging import log


class TabLog(QWidget):
    LEVELS = [
        log.WARNING,
        log.INFO,
        log.DEBUG,
    ]

    def __init__(self):
        super().__init__()
        self._init_style()
        self._add_widgets()
        self._connect_widget_signals()

    def _init_style(self):
        pass

    def _add_widgets(self):
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._create_log_level())
        layout.addWidget(self._create_log_list())
        super().setLayout(layout)
        self._update_log()

    def _create_log_level(self):
        self._log_level = QComboBox()
        self._log_level.addItems([
            "warnings and errors",
            "informational",
            "debug messages",
        ])
        return self._log_level

    def _create_log_list(self):
        self._log_list = QPlainTextEdit()
        self._log_list.setReadOnly(True)
        return self._log_list

    def _connect_widget_signals(self):
        self._log_level.currentIndexChanged.connect(self._update_log)

    def _update_log(self):
        level = self.LEVELS[self._log_level.currentIndex()]
        text = "\n".join([
            f"{log.level_name(lev)}: {msg}"
            for (lev, msg) in log.contents(level)
        ])
        self._log_list.setPlainText(text)
