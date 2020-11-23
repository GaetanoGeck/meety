from PyQt5.QtWidgets import QLineEdit


class SearchWidget(QLineEdit):
    def __init__(self):
        super().__init__()
        super().setPlaceholderText("search")
        super().setProperty("class", "search")
