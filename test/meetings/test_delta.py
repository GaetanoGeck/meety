from datetime import datetime

import pytest
import testdata

from meety.meetings.preferences import (
    DateInterval,
    DisjunctiveIntervals,
    TimeInterval,
    reset_options,
)

delta_data = testdata.load(["meetings", "test_delta.yaml"])


@pytest.mark.parametrize("spec, config, tests", [
    (c["spec"], c["config"], c["tests"])
    for c in delta_data.get("date") or []
])
def test_date_delta(spec, config, tests):
    reset_options()
    interval = DisjunctiveIntervals.parse_date(spec)
    DateInterval.set_options(config)
    for test in tests:
        test_date = test["test_date"]
        test_time = test.get("test_time")
        test_date = testdata.str_to_date(test_date)
        expected = test["expected"]
        if test_time:
            test_time = testdata.str_to_time(test_time)
            test_date = datetime.combine(test_date, test_time)
        assert str(interval.is_satisfied(test_date)) == expected


@pytest.mark.parametrize("spec, config, tests", [
    (
        c["spec"],
        c["config"],
        c["tests"],
    )
    for c in delta_data.get("time") or []
])
def test_time_delta(spec, config, tests):
    reset_options()
    interval = DisjunctiveIntervals.parse_time(spec)
    TimeInterval.set_options(config)
    for test in tests:
        test_time = test["test_time"]
        expected = test["expected"]
        test_time = testdata.str_to_time(test_time)
        test_date = datetime.combine(datetime.today(), test_time)
        assert str(interval.is_satisfied(test_date)) == expected
