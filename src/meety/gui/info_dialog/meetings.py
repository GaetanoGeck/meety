from PyQt5.QtWidgets import QPlainTextEdit


class TabMeetings(QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self._init_style()
        self._add_widgets()
        self._connect_widget_signals()

    def _init_style(self):
        pass

    def _add_widgets(self):
        super().setReadOnly(True)
        self._update_meetings()

    def _update_meetings(self):
        from meety.gui.app import get_all_meetings
        meetings = get_all_meetings()
        text = "\n".join([m.debug_info() for m in meetings])
        if not text:
            text = "There are no meetings!"
        super().setPlainText(text)

    def _connect_widget_signals(self):
        pass
