from PyQt5.QtCore import (
    QEvent,
    QMargins,
    QRect,
    Qt,
    pyqtSignal,
)
from PyQt5.QtGui import (
    QBrush,
    QColor,
    QFont,
    QPen,
)
from PyQt5.QtWidgets import (
    QApplication,
    QItemDelegate,
    QStyle,
    QStyleOptionButton,
)

from meety.gui import styles


class ItemDelegate(QItemDelegate):
    """Draw meeting items according to their match status and the GUI
    configuration.
    """

    context_menu_requested = pyqtSignal(object, name="context_menu_requested")

    def __init__(self, parent=None, *args):
        QItemDelegate.__init__(self, parent, *args)
        self._context_menu_button_rects = {}

    def paint(self, painter, option, index):
        painter.save()
        self._draw_background(painter, option, index)
        self._draw_border(painter, option)
        self._draw_context_menu_button(painter, option, index)
        self._draw_text(painter, option, index)
        painter.restore()

    def editorEvent(self, event, model, option, index):
        if event.type() == QEvent.MouseButtonRelease:
            rect = self._context_menu_button_rects[index]
            if rect.contains(event.pos()):
                self.context_menu_requested.emit(event)
                return True
        return super().editorEvent(event, model, option, index)

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

    def _draw_context_menu_button(self, painter, option, index):
        style = QStyleOptionButton()
        style.features = QStyleOptionButton.Flat
        style.rect = self._context_menu_button_rect(option, index)
        style.text = "☰"
        style.state = QStyle.State_Enabled

        painter.setPen(QColor("blue"))
        QApplication.style().drawControl(
            QStyle.CE_PushButton,
            style,
            painter
        )

    def _context_menu_button_rect(self, option, index):
        anchor = option.rect.bottomRight()
        margins = QMargins(3, 3, 3, 3)
        rect = QRect(0, 0, 30, 30)
        rect.moveBottomRight(anchor)
        self._context_menu_button_rects[index] = rect
        return rect.marginsRemoved(margins)

    @classmethod
    def _draw_text(cls, painter, option, index):
        rmeeting = index.data(Qt.UserRole)
        rect = option.rect.marginsRemoved(QMargins(5, 5, 5, 0))
        cls._draw_text_name(painter, rect, rmeeting)
        cls._draw_text_info(painter, rect, rmeeting)

    @classmethod
    def _draw_text_name(cls, painter, rect, rmeeting):
        title = rmeeting.meeting.name
        cls._set_font_properties(painter, rmeeting.match_style)
        painter.drawText(rect, Qt.AlignLeft, title)

    @classmethod
    def _draw_text_info(cls, painter, rect, rmeeting):
        info = rmeeting.match_preference_details
        if info and styles.get_show("info"):
            cls._set_font_properties(painter, "info")
            painter.drawText(rect, Qt.AlignLeft | Qt.AlignBottom, info)

    @classmethod
    def _set_font_properties(cls, painter, style):
        cls._set_font_color(painter, style)
        cls._set_font(painter, style)

    @classmethod
    def _set_font_color(cls, painter, style):
        color = styles.get_color(style)
        painter.setPen(QPen(QColor(color)))

    @classmethod
    def _set_font(cls, painter, style):
        font = QFont()
        font.setPixelSize(styles.get_font_size(style))
        font.setBold(styles.is_bold(style))
        painter.setFont(font)
