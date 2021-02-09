from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QWidget,
)

from meety.gui.info_dialog import InfoDialog


class StatusWidget(QWidget):
    NOTIFY_QUICK_TIME_SPAN = 3000
    NOTIFY_NORMAL_TIME_SPAN = 8000
    WARNING_TIME_SPAN = 10000

    def __init__(self):
        super().__init__()
        self._message_queue = []
        self._init_style()
        self._add_widgets()
        self._connect_widget_signals()
        self.show_default_message()

    def _init_style(self):
        pass

    def _add_widgets(self):
        layout = self._create_layout()
        layout.addWidget(self._create_status(), 1)
        layout.addWidget(self._create_info(), 0)
        self.setLayout(layout)

    def _create_layout(self):
        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        return layout

    def _create_status(self):
        self._status = QLabel("")
        return self._status

    def _create_info(self):
        self._info = QPushButton("&info")
        self._info.setToolTip(
            "Show logs, loaded data and version information."
        )
        self._info.setProperty("class", "info")
        return self._info

    def _connect_widget_signals(self):
        self._info.clicked.connect(self.show_info)
        self._timer = QTimer()
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self._show_next_message)

    def show_default_message(self):
        self._status.setText("Ready.")

    def notify_quickly(self, text):
        span = self.NOTIFY_QUICK_TIME_SPAN
        self._enqueue_notification(text, "", span)

    def notify(self, text, tooltip=""):
        span = self.NOTIFY_NORMAL_TIME_SPAN
        self._enqueue_notification(text, tooltip, span)

    def warn(self, text, tooltip=""):
        span = self.WARNING_TIME_SPAN
        self._enqueue_notification(f"Warning: {text}", tooltip, span)

    def _enqueue_notification(self, text, tooltip, time_span):
        self._message_queue.append((text, tooltip, time_span))
        if len(self._message_queue) == 1:
            self._show_message()

    def _show_next_message(self):
        self._message_queue.pop(0)
        if self._message_queue:
            self._show_message()
        else:
            self.show_default_message()

    def _show_message(self):
        text, tooltip, time_span = self._message_queue[0]
        self._status.setText(text)
        self._status.setToolTip(tooltip)
        self._timer.start(time_span)

    def clear_notifications(self):
        if self._message_queue:
            self._timer.stop()
            self._message_queue.clear()
            self.show_default_message()

    def show_info(self):
        dialog = InfoDialog()
        dialog.exec_()
