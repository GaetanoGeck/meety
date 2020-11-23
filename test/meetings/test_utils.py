import pytest

from meety.meetings import utils


@pytest.mark.parametrize("expected, text", [
    ([], ""),
    ([["1"]], "1"),
    ([["1"], ["2"]], "1,2"),
    ([["1"], ["2"], ["3"]], "1,2,3"),
    ([["1", "2"]], "1 - 2"),
    ([["1 - 2 - 3"]], "1 - 2 - 3"),
    ([["1", "2"], ["3", "4"]], "1 - 2,3 - 4"),
    ([["1", "2"], ["3"], ["4", "5"]], "1 - 2,3,4 - 5"),
    # date ranges:
    (
        [["2020-01-02"], ["2020-03-04", "2020-05-06"]],
        "2020-01-02, 2020-03-04 - 2020-05-06"
    ),
    (
        [["2020-01-02"], ["2020-03-04", "2020-05-06"]],
        "2020-01-02, 2020-03-04-2020-05-06"
    ),
])
def test_list_of_ranges(expected, text):
    assert expected == utils.list_of_ranges(text)


def test_to_pair_from_singleton():
    assert (1, 1) == utils.to_pair([1])
    assert (2, 2) == utils.to_pair([2])


def test_to_pair_from_double():
    assert (1, 2) == utils.to_pair([1, 2])
    assert (2, 3) == utils.to_pair([2, 3])


def test_to_pair_from_too_many():
    assert (8, 9) == utils.to_pair([1, 2, 3], (8, 9))
    assert (None, None) == utils.to_pair([1, 2, 3])
    assert (8, 9) == utils.to_pair([1, 2, 3, 4], (8, 9))
    assert (None, None) == utils.to_pair([1, 2, 3, 4])
