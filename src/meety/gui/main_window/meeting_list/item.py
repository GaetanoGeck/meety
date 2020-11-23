from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListWidgetItem


class MeetingItem(QListWidgetItem):
    def __init__(self, rmeeting):
        self._rmeeting = rmeeting
        super().__init__(self.name)
        self._init_style()
        self._init_meta_data()

    def _init_style(self):
        pass

    def _init_meta_data(self):
        for role, value in [
            (Qt.DisplayRole, self.name),
            (Qt.UserRole, self.rated_meeting),
            (Qt.ToolTipRole, self.info),
        ]:
            self.setData(role, value)

    @property
    def rating(self):
        return self._rmeeting.rating

    @property
    def meeting(self):
        return self._rmeeting.meeting

    @property
    def rated_meeting(self):
        return self._rmeeting

    @property
    def name(self):
        return self.meeting.name

    @property
    def info(self):
        return self.meeting.data_to_str()
