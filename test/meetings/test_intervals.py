from datetime import datetime

import pytest
import testdata

from meety.meetings.preferences import (
    FALSE_INTERVAL,
    TRUE_INTERVAL,
    DisjunctiveIntervals,
    reset_options,
)

interval_config = testdata.load(["meetings", "test_intervals.yaml"])


def test_empty_disjunctive_interval_is_satisfied():
    interval = DisjunctiveIntervals([])
    assert interval.is_satisfied(datetime.now())


def test_false_interval_does_not_match():
    assert not FALSE_INTERVAL.match(datetime.now())


def test_true_interval_is_satisfied():
    assert TRUE_INTERVAL.match(datetime.now())


@pytest.mark.parametrize("text, tests", [
    (c["text"], c["tests"])
    for c in interval_config.get("date_interval_parse") or []
])
def test_date_interval_parse(text, tests):
    reset_options()
    interval = DisjunctiveIntervals.parse_date(text)
    for test in tests:
        date = test["date"]
        expected_match = test["expected"]
        result = interval.is_satisfied(testdata.str_to_date(date))
        assert str(result) == expected_match


@pytest.mark.parametrize("text, tests", [
    (c["text"], c["tests"])
    for c in interval_config.get("time_interval_parse") or []
])
def test_time_interval_parse(text, tests):
    reset_options()
    interval = DisjunctiveIntervals.parse_time(text)
    for test in tests:
        datetime = test["datetime"]
        expected_match = test["expected"]
        result = interval.is_satisfied(testdata.str_to_datetime(datetime))
        assert str(result) == expected_match


@pytest.mark.parametrize("text, tests", [
    (c["text"], c["tests"])
    for c in interval_config.get("weekday_interval_parse") or []
])
def test_weekday_interval_parse(text, tests):
    reset_options()
    testdata.apply_language_configurations("lang_en")
    interval = DisjunctiveIntervals.parse_weekday(text)
    for test in tests:
        datetime = test["date"]
        expected_match = test["expected"]
        result = interval.is_satisfied(testdata.str_to_date(datetime))
        assert str(result) == expected_match
