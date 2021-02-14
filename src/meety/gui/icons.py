from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon

from meety import resources


def get_icon(name, sizes=[256]):
    icon = QIcon()
    for size in sizes:
        filename = f"{name}-{size}.png"
        _add_file_to_icon(icon, filename, size)
    return icon


def _add_file_to_icon(icon, filename, size):
    path = resources.get_icon_path(filename)
    icon.addFile(str(path), QSize(size, size))
