import os

from PyQt5.QtWidgets import (
    QButtonGroup,
    QFileDialog,
    QGridLayout,
    QGroupBox,
    QLineEdit,
    QPushButton,
    QRadioButton,
    QVBoxLayout,
    QWidget,
)

last_path = None


class AddModeWidget(QGroupBox):
    def __init__(self):
        super().__init__("Mode")
        self._init_style()
        self._add_widgets()
        self._connect_widget_signals()
        self._init_state()

    def _init_style(self):
        pass

    def _add_widgets(self):
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        mode_group = QButtonGroup(self)
        layout.addWidget(self._create_add_session(mode_group))
        layout.addWidget(self._create_add_file(mode_group))
        super().setLayout(layout)

    def _create_add_session(self, mode_group):
        self._mode_add_session = self._new_option(
            mode_group,
            "add temporarily",
            "Meeting entry is kept only until program termination."
        )
        return self._mode_add_session

    def _create_add_file(self, mode_group):
        self._mode_file = self._new_option(
            mode_group,
            "add to YAML-file",
            "Meeting entry will be saved in the specified YAML file."
        )
        self._file_path = QLineEdit()
        self._file_path.setPlaceholderText("Path")
        if last_path:
            self._file_path.setText(last_path)
        self._file_choose = QPushButton("ch&oose")
        self._file_choose.setToolTip("Select path via file dialog")
        w = QWidget()
        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._mode_file, 0, 0, 2, 1)
        layout.addWidget(self._file_path, 2, 0)
        layout.addWidget(self._file_choose, 2, 1)
        w.setLayout(layout)
        return w

    def _new_option(self, mode_group, label, tooltip):
        btn = QRadioButton(label)
        btn.setToolTip(tooltip)
        mode_group.addButton(btn)
        return btn

    def _connect_widget_signals(self):
        self._mode_add_session.toggled.connect(self._on_toggled)
        self._mode_file.toggled.connect(self._on_toggled)
        self._file_choose.clicked.connect(self._choose_path)
        self._file_path.textChanged.connect(self._on_path_changed)

    def _on_toggled(self):
        file_mode = self._mode_file.isChecked()
        self._file_path.setEnabled(file_mode)
        self._file_choose.setEnabled(file_mode)

    def _on_path_changed(self, text):
        global last_path
        last_path = text

    def _choose_path(self):
        path = self._ask_for_filename()
        if path:
            self._file_path.setText(path)

    def _ask_for_filename(self):
        filename = QFileDialog.getSaveFileName(
            parent=QFileDialog(),
            caption="Meeting specification file",
            directory=os.path.expanduser("~"),
            filter="yaml (*.yaml *.yml)"
        )[0]
        return filename

    def _init_state(self):
        self._mode_add_session.setChecked(True)
        self._on_toggled()

    def is_mode_temporary(self):
        return self._mode_add_session.isChecked()

    def file_path(self):
        if not self.is_mode_temporary():
            return self._file_path.text()
