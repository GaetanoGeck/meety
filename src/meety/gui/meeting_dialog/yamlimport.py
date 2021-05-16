from PyQt5.QtWidgets import (
    QLabel,
    QPlainTextEdit,
    QVBoxLayout,
    QWidget,
)


class YamlImport(QWidget):
    def __init__(self, text=""):
        super().__init__()
        self._init_style()
        self._add_widgets()
        self._connect_widget_signals()
        self._yaml_spec.setPlainText(text)

    def _init_style(self):
        pass

    def _add_widgets(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(QLabel("YAML meeting specification:"))
        layout.addWidget(self._create_yaml_spec())
        self.setLayout(layout)

    def _create_yaml_spec(self):
        self._yaml_spec = QPlainTextEdit()
        return self._yaml_spec

    def _connect_widget_signals(self):
        pass

    def setSpecification(self, spec):
        self._yaml_spec.setPlainText(spec)

    def specification(self):
        return self._yaml_spec.toPlainText()
