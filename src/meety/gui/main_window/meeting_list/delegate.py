from PyQt5.QtCore import (
    QMargins,
    Qt,
)
from PyQt5.QtGui import (
    QBrush,
    QColor,
    QFont,
    QPen,
)
from PyQt5.QtWidgets import (
    QItemDelegate,
    QStyle,
)

from meety.gui import styles


class ItemDelegate(QItemDelegate):
    """Draw meeting items according to their match status and the GUI
    configuration.
    """

    def __init__(self, parent=None, *args):
        QItemDelegate.__init__(self, parent, *args)

    @classmethod
    def paint(cls, painter, option, index):
        painter.save()
        cls._draw_background(painter, option, index)
        cls._draw_border(painter, option)
        cls._draw_text(painter, option, index)
        painter.restore()

    def sizeHint(self, option, index):
        orig_size = super().sizeHint(option, index)
        return orig_size.grownBy(QMargins(5, 10, 5, 15))

    @classmethod
    def _draw_background(cls, painter, option, index):
        painter.setPen(QPen(Qt.NoPen))
        cls._set_bg_color(painter, option, index)
        painter.drawRect(option.rect)

    @classmethod
    def _set_bg_color(cls, painter, option, index):
        rmeeting = index.data(Qt.UserRole)
        if option.state & QStyle.State_Selected:
            color = styles.get_selected(rmeeting.match_style)
        else:
            color = styles.get_background(rmeeting.match_style)
        painter.setBrush(QBrush(QColor(color)))

    @classmethod
    def _draw_border(cls, painter, option):
        painter.setPen(QPen(QColor(styles.get_border_color())))
        painter.drawLine(
            option.rect.bottomLeft(),
            option.rect.bottomRight()
        )

    @classmethod
    def _draw_text(cls, painter, option, index):
        rmeeting = index.data(Qt.UserRole)
        title = rmeeting.meeting.name
        rect = option.rect.marginsRemoved(QMargins(5, 5, 5, 0))
        cls._set_font_properties(painter, rmeeting)
        painter.drawText(rect, Qt.AlignLeft, title)

    @classmethod
    def _set_font_properties(cls, painter, rmeeting):
        cls._set_font_color(painter, rmeeting)
        cls._set_font_weight(painter, rmeeting)

    @classmethod
    def _set_font_color(cls, painter, rmeeting):
        color = styles.get_color(rmeeting.match_style)
        painter.setPen(QPen(QColor(color)))

    @classmethod
    def _set_font_weight(cls, painter, rmeeting):
        font = QFont()
        font.setBold(styles.is_bold(rmeeting.match_style))
        painter.setFont(font)
