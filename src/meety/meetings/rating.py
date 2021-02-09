import datetime

from meety.meetings.preferences import TimeMatchDescription


class RatedMeeting:
    """A meeting with its time preference and query ratings."""

    PREFER_FACTOR = 1
    QUERY_FACTOR = 10

    def __init__(self, meeting):
        """Save meeting with preference and query rating."""
        self._meeting = meeting
        self._prating = TimeMatchDescription.NOT_MATCHING
        self._qrating = False

    @property
    def meeting(self):
        return self._meeting

    def set_preference_rating(self, prating):
        self._prating = prating

    def set_query_rating(self, qrating):
        self._qrating = qrating

    @property
    def rating(self):
        """Compute total rating value."""
        return sum([
            RatedMeeting.PREFER_FACTOR * self._prating.value,
            RatedMeeting.QUERY_FACTOR * self._qrating,
        ])

    def matches_query(self):
        return self._qrating

    def matches_preference(self):
        return TimeMatchDescription.matches(self._prating)

    def matches(self):
        return self.rating > 0

    @property
    def match_style(self):
        if self.matches_query():
            return "matching_query"
        if self.matches_preference():
            return "matching_preference"
        return "others"

    @property
    def match_preference_details(self):
        return {
            TimeMatchDescription.TIME_MATCHING: "now",
            TimeMatchDescription.DATE_MATCHING: "today",
            TimeMatchDescription.WEEKDAY_MATCHING: "today",
        }.get(self._prating, "")

    def __str__(self):
        return str(self._meeting)

    def debug_info(self):
        name = str(self._meeting)
        if self.matches_query():
            status = "Q"
        elif self.matches_preference():
            status = "T"
        else:
            status = "x"
        return f"{self.rating:3d} {status} {name}"


class Ratings:
    """All meetings and their ratings."""

    @classmethod
    def rate_meeting(cls, meeting, iquery, when):
        rmeeting = RatedMeeting(meeting)
        rmeeting.set_preference_rating(meeting.match_time(when))
        rmeeting.set_query_rating(meeting.match_query(iquery))
        return rmeeting

    def __init__(self, meetings):
        """Start without ratings."""
        self._meetings = meetings
        self._rated_meetings = []

    def rate(self, query, when=None):
        """Rate all meetings based on the `query` and the provided
        datetime `when` (or current time, by default).
        """
        if when is None:
            when = datetime.datetime.now()
        matches = self._rate_meetings(query, when)
        self._rated_meetings = sorted(
            matches,
            key=lambda m: m.rating,
            reverse=True,
        )

    def _rate_meetings(self, query, when):
        return [
            Ratings.rate_meeting(m, query, when)
            for m in self._meetings
        ]

    def get_all(self):
        """Return all meetings."""
        return self._rated_meetings

    def get_all_matching(self):
        """Return only meetings with a positive rating."""
        return [rm for rm in self._rated_meetings if rm.rating > 0]

    def get_only_best(self):
        """Return only meetings with a maximal rating."""
        if self._rated_meetings:
            best_rating = self._rated_meetings[0].rating
            return [
                rm for rm in self._rated_meetings
                if rm.rating >= best_rating
            ]

    def get_only_first(self):
        """Get only the first meeting (with a maximal rating)."""
        if self._rated_meetings:
            return [self._rated_meetings[0]]
