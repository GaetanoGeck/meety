import os
import shutil

from PyQt5.QtWidgets import (
    QFileDialog,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from meety import (
    io,
    resources,
)
from meety.gui import app


def TEMPLATE_CREATED_MSG(target):
    return f'''<b>Template file created!</b> Next, please
    <ol>
        <li>edit the file <a href="{target}">{target}</a>
        according to your needs and</li>

        <li>reload the changed specification
        <ul>
            <li>via the context menu or</li>
            <li>by restarting the application.</li>
        </ul>
        </li>
    </ol>
    '''


class TabFiles(QWidget):
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
        layout.addWidget(self._create_status())
        layout.addStretch(1)
        layout.addWidget(self._create_template_label())
        layout.addWidget(self._create_template_button())
        self.setLayout(layout)

    def _create_template_label(self):
        self._template_label = QLabel("<hr>")
        self._template_label.setWordWrap(True)
        return self._template_label

    def _create_template_button(self):
        self._template_button = QPushButton(
            "&Create specification from template"
        )
        self._template_button.setToolTip(
            "You can create a new meeting specification "
            "by editing a template. Click this button to "
            "save the template in a file."
        )
        self._template_button.setProperty("class", "create_template")
        return self._template_button

    def _create_status(self):
        self._status = QLabel(self.status)
        self._status.setOpenExternalLinks(True)
        return self._status

    def _connect_widget_signals(self):
        self._template_button.clicked.connect(self._create_template)

    def _create_template(self):
        source = resources.get_spec_path("example.yaml")
        target = self._ask_for_filename()
        if not target:
            return

        msg = QMessageBox()
        try:
            shutil.copy(source, target)
        except Exception as e:
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Error on template creation.")
            msg.setDetailedText(str(e))
        else:
            app.add_meeting_file(target)
            msg.setIcon(QMessageBox.Information)
            msg.setText(TEMPLATE_CREATED_MSG(target))
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def _ask_for_filename(self):
        filename = QFileDialog.getSaveFileName(
            parent=QFileDialog(),
            caption="New meeting specification",
            directory=os.path.expanduser("~"),
            filter="yaml (*.yaml *.yml)"
        )[0]
        return filename

    @property
    def status(self):
        return f"{self.status_directories}<br/>{self.status_files}"

    @property
    def status_directories(self):
        status = "<b>Considered directories:</b> "
        paths = app.get_active_directories()
        if paths:
            stats = [self.status_directory(p) for p in paths]
            status += io.html.unordered_list(stats)
        else:
            status += "no directories"
        return status

    def status_directory(self, path):
        return f'<a href="{path}">{path}</a>'

    @property
    def status_files(self):
        status = "<b>Considered files:</b> "
        loaded_paths = app.get_loaded_paths()
        paths = loaded_paths.all_paths
        if paths:
            stats = [
                self.status_file(p, loaded_paths.status(p))
                for p in paths
            ]
            status += io.html.unordered_list(stats)
        else:
            status += "no files"
        return status

    def status_file(self, path, info):
        link = f'<a href="{path}">{path}</a>'
        info = f'<i>({info})</i>'
        return f"{link} {info}"
