import pytest
import testdata

from meety import io
from meety.loader import Loader
from meety.meetings.rating import (
    RatedMeeting,
    Ratings,
)

test_config = testdata.load(["meetings", "test_rating.yaml"])


@pytest.mark.parametrize("filename, query, query_type, rated", [
    (
        c["file"],
        c["query"],
        c.get("type", "all-matching"),
        c["rated"]
    ) for c in test_config
])
def test_rating(filename, query, query_type, rated):
    loader = Loader()
    loader.load_from_file(testdata.testpath(["data", filename]))
    io.reset_options()

    r = Ratings(loader.meetings)
    RatedMeeting.PREFER_FACTOR = 0
    r.rate(query)
    rmeetings = {
        "all": r.get_all(),
        "all-matching": r.get_all_matching(),
        "only-best": r.get_only_best(),
        "only-first": r.get_only_first(),
    }[query_type]

    assert [m.meeting.name for m in rmeetings] == rated
