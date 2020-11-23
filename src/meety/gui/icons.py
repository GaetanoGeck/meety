import importlib.resources as resources

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon

from meety.static import icons as static_icons


def get_icon(name, sizes=[256]):
    icon = QIcon()
    for size in sizes:
        filename = f"{name}-{size}.png"
        _add_file_to_icon(icon, filename, size)
    return icon


def _add_file_to_icon(icon, filename, size):
    with resources.path(static_icons, filename) as path:
        icon.addFile(str(path), QSize(size, size))
