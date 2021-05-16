from PyQt5.QtWidgets import (
    QDialog,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)

from meety.gui import app
from meety.gui.meeting_dialog.addmode import AddModeWidget
from meety.gui.meeting_dialog.yamlimport import YamlImport


class MeetingDialog(QDialog):
    def __init__(self, text=""):
        super().__init__()
        self.setWindowTitle("Add meeting")
        self._init_style()
        self._add_widgets()
        self._connect_widget_signals()
        self._yaml_spec.setSpecification(text)

    def _init_style(self):
        pass

    def _add_widgets(self):
        layout = QVBoxLayout()
        layout.addWidget(self._create_yaml_spec())
        layout.addWidget(self._create_add_mode())
        layout.addWidget(self._create_add_button())
        self.setLayout(layout)

    def _create_yaml_spec(self):
        self._yaml_spec = YamlImport()
        return self._yaml_spec

    def _create_add_mode(self):
        self._add_mode = AddModeWidget()
        return self._add_mode

    def _create_add_button(self):
        self._add_button = QPushButton("Add &meeting")
        return self._add_button

    def _connect_widget_signals(self):
        self._add_button.clicked.connect(self._on_add_meeting),

    def _on_add_meeting(self):
        yaml = self._yaml_spec.specification()
        error = self._check_yaml_for_error(yaml)
        if error:
            self._show_error(error)
            return
        if self._add_mode.is_mode_temporary():
            self._add_meetings_temporarily(yaml)
        else:
            path = self._add_mode.file_path()
            self._add_meetings_to_file(yaml, path)

    def _check_yaml_for_error(self, yaml):
        if not yaml:
            return "YAML specification is empty!"

    def _add_meetings_temporarily(self, yaml):
        app.add_meeting_specs(yaml)
        self._show_success(f"Updated meeting list!")

    def _add_meetings_to_file(self, yaml, path):
        with open(path, "a") as yaml_file:
            yaml_file.write(f"\n{yaml}\n")
        app.add_meeting_file(path)
        self._show_success(
            f"Appended specification to file '{path}' and"
            " updated meeting list!"
        )

    def _show_error(self, text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText(text)
        msg.exec_()

    def _show_success(self, text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(text)
        msg.exec_()
