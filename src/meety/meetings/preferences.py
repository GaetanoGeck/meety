""" Time preferences that can comprise weekday, date and time specifications.
Each specification can be a scalar, a range or a list of ranges.
"""
import enum
from abc import (
    ABC,
    abstractmethod,
)
from datetime import (
    datetime,
    time,
    timedelta,
)
from functools import total_ordering

from meety import io
from meety.logging import log
from meety.meetings import utils


def reset_options():
    WeekdayInterval.reset_options()
    DateInterval.reset_options()
    TimeInterval.reset_options()
    io.reset_options()


def set_options(config, name):
    WeekdayInterval.set_options(config.get("weekday") or {})
    DateInterval.set_options(config.get("date") or {})
    TimeInterval.set_options(config.get("time") or {})
    io.datetime.set_options(config, name)


def to_datetime(d, t):
    try:
        return datetime.combine(d, t)
    except TypeError:
        return None


@total_ordering
class TimeMatchDescription(enum.Enum):
    NOT_MATCHING = 0
    NOT_DEFINED = 1
    MATCHING = 2
    WEEKDAY_MATCHING = 3
    DATE_MATCHING = 4
    TIME_MATCHING = 5

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented

    def matches(description):
        return description not in [
            TimeMatchDescription.NOT_MATCHING,
            TimeMatchDescription.NOT_DEFINED,
        ]


class TimePreference:
    """Each time preference can refer to weekday, date and time conditions.
    The conditions can be lists of ranges.
    """

    @classmethod
    def from_dict(cls, data):

        def _parse_or_true(name, parser):
            att = data.get(name)
            if att:
                return parser(att)
            else:
                return TRUE_DISJUNCTION

        weekday = _parse_or_true("weekday", DisjunctiveIntervals.parse_weekday)
        date = _parse_or_true("date", DisjunctiveIntervals.parse_date)
        time = _parse_or_true("time", DisjunctiveIntervals.parse_time)
        return TimePreference(weekday=weekday, date=date, time=time)

    @classmethod
    def from_str(cls, text):

        def _parse_tokens(parser):
            return io.parse_first_possible(parser, tokens)

        tokens = io.split_on_semicolon_or_comma(text)
        weekday = _parse_tokens(DisjunctiveIntervals.parse_weekday)
        date = _parse_tokens(DisjunctiveIntervals.parse_date)
        time = _parse_tokens(DisjunctiveIntervals.parse_time)
        return TimePreference(weekday=weekday, date=date, time=time)

    def __init__(self, weekday, date, time):
        self._weekday = weekday
        self._date = date
        self._time = time

    def match(self, when):
        """Tests whether all conditions (weekday, time, date) are met."""
        subconditions = [
            p.is_satisfied(when, description)
            for name, p, description in self._named_and_weighted_preferences
        ]
        if TimeMatchDescription.NOT_MATCHING in subconditions:
            # not all conditions are matched
            return TimeMatchDescription.NOT_MATCHING
        else:
            # consider the strongest condition
            return max(subconditions)

    def __str__(self):
        prefs = [p for p in self._named_and_weighted_preferences if str(p[1])]
        if len(prefs) == 0:
            return "no preference"

        def describe(name, pref):
            return f"      {name}: {pref}"

        if len(prefs) == 1:
            return describe(prefs[0])
        else:
            return "\n".join([describe(n, p) for (n, p, w) in prefs])

    @property
    def is_nontrivial(self):
        p = list(self._named_and_weighted_preferences)
        return len(p) > 0

    @property
    def _named_and_weighted_preferences(self):
        if self._weekday:
            yield (
                "weekday",
                self._weekday,
                TimeMatchDescription.WEEKDAY_MATCHING
            )
        if self._date:
            yield (
                "date",
                self._date,
                TimeMatchDescription.DATE_MATCHING
            )
        if self._time:
            yield (
                "time",
                self._time,
                TimeMatchDescription.TIME_MATCHING
            )


class DisjunctiveIntervals:
    """A list of intervals that are considered as alternatives."""

    @classmethod
    def parse_weekday(cls, text, warn=True):
        return DisjunctiveIntervals(cls.parse(WeekdayInterval, text, warn))

    @classmethod
    def parse_date(cls, text, warn=True):
        return DisjunctiveIntervals(cls.parse(DateInterval, text, warn))

    @classmethod
    def parse_time(cls, text, warn=True):
        return DisjunctiveIntervals(cls.parse(TimeInterval, text, warn))

    @classmethod
    def parse(cls, interval_cls, text, warn=True):
        if text is None:
            return None
        clean_text = io.datetime.prepare_list_of_ranges(text)
        ranges = utils.list_of_ranges(clean_text)
        intervals = []
        for r in ranges:
            try:
                interval = interval_cls.parse(r, warn)
            except ValueError:
                log.warning(f"Cannot parse '{r}' in '{text}'.", warn)
            else:
                if interval and interval.is_valid:
                    intervals.append(interval)
        return intervals or None

    def __init__(self, intervals):
        self._intervals = intervals

    @property
    def is_valid(self):
        return self._intervals

    def is_satisfied(self, when, desc=TimeMatchDescription.NOT_MATCHING):
        """Tests whether the given `when` satisfies at least one
        interval or whether there is none.
        """
        if self._intervals is None:
            return TimeMatchDescription.NOT_MATCHING
        if not self._intervals:
            return TimeMatchDescription.NOT_DEFINED
        return desc if any(self.match_all(when)) \
            else TimeMatchDescription.NOT_MATCHING

    def match_all(self, when):
        """Apply matching test for `when` to each interval."""
        return map(lambda i: i.match(when), self._intervals)

    def __str__(self):
        """Return a comma-separated list of the intervals."""
        if not self._intervals:
            return "<UNDEFINED>"
        return ", ".join([str(i) for i in self._intervals])


FALSE_DISJUNCTION = DisjunctiveIntervals(None)
TRUE_DISJUNCTION = DisjunctiveIntervals([])


class AbstractInterval(ABC):
    """Common functionality for weekday, date and time intervals."""

    @classmethod
    def reset_options(cls):
        cls._start_delta = timedelta()
        cls._end_delta = timedelta()

    @classmethod
    def set_options(cls, config):
        if config:
            sdelta = config.get("start_delta")
            if sdelta:
                cls._start_delta = io.datetime.parse_timedelta(sdelta)
            edelta = config.get("end_delta")
            if edelta:
                cls._end_delta = io.datetime.parse_timedelta(edelta)

    @classmethod
    def parse(cls, entries, warn=True):
        clean_entries = [e.strip().casefold() for e in entries]
        stext, etext = utils.to_pair(clean_entries)
        start = cls._parse_entry(stext, warn)
        end = cls._parse_entry(etext, warn)
        return cls(start or end, end or start)

    @classmethod
    @abstractmethod
    def _parse_entry(cls, entry, warn=True):
        pass

    @classmethod
    @abstractmethod
    def _entry_to_string(cls, entry):
        pass

    def __init__(self, start, end):
        self._start = start
        self._end = end

    @property
    def is_valid(self):
        return None not in [self._start, self._end]

    @abstractmethod
    def match(self, when):
        pass

    def _is_between_datetime(self, start, when, end):
        try:
            lower = start + self._start_delta
            upper = end + self._end_delta
            return lower <= when <= upper
        except TypeError:
            return False

    def __str__(self):
        stext = self._entry_to_string(self._start)
        etext = self._entry_to_string(self._end)
        if stext == etext:
            return stext
        else:
            return "%s - %s" % (stext, etext)


class ConstantInterval(AbstractInterval):
    def __init__(self, value):
        super().__init__(None, None)
        self._value = value

    def match(self, when):
        return self._value

    @classmethod
    def _parse_entry(cls, entry, warn=True): pass

    @classmethod
    def _entry_to_string(cls, entry):
        return "<CONSTANT>"


FALSE_INTERVAL = ConstantInterval(False)
TRUE_INTERVAL = ConstantInterval(True)


class DateInterval(AbstractInterval):
    """An interval of dates.
    For instance, '2020-05-27' or '2020-05-27 - 2020-05-30'.
    """

    _start_delta = timedelta()
    _end_delta = timedelta()

    def __init__(self, start, end):
        super().__init__(start, end)

    def match(self, when):
        lower = to_datetime(self._start, time(0, 0))
        upper = to_datetime(self._end, time(23, 59))
        return self._is_between_datetime(lower, when, upper)

    @classmethod
    def _parse_entry(cls, text, warn=True):
        return io.datetime.parse_date(text, warn)

    @classmethod
    def _entry_to_string(cls, entry):
        return io.datetime.date_to_str(entry)


class TimeInterval(AbstractInterval):
    """An interval of times.
    For instance, '20:15' or '20:15 - 21:45'.
    """

    _start_delta = timedelta()
    _end_delta = timedelta()

    def __init__(self, start, end):
        super().__init__(start, end)

    def match(self, when):
        start = to_datetime(when.date(), self._start)
        end = to_datetime(when.date(), self._end)
        return self._is_between_datetime(start, when, end)

    @classmethod
    def _parse_entry(cls, text, warn):
        return io.datetime.parse_time(text, warn)

    @classmethod
    def _entry_to_string(cls, entry):
        return io.datetime.time_to_str(entry)


class WeekdayInterval(AbstractInterval):
    """An interval of weekdays.
    For instance,  'Sunday' or 'Monday - Friday'.
    """

    def __init__(self, start, end):
        super().__init__(start, end)

    def match(self, when):
        start = self._start
        day = when.isoweekday()
        end = self._end
        return self._is_between_days(start, day, end)

    def _is_between_days(self, start, when, end):
        try:
            return start <= when <= end
        except TypeError:
            return False

    @classmethod
    def _parse_entry(cls, text, warn=True):
        return io.datetime.parse_weekday(text, warn)

    @classmethod
    def _entry_to_string(cls, entry):
        return io.datetime.weekday_to_str(entry)
