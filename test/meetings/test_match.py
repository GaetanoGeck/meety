import pytest
import testdata

from meety.meetings import preferences
from meety.meetings.preferences import TimePreference

match_config_general = testdata.load(["meetings", "test_match.yaml"])
match_config_en = testdata.load(["meetings", "test_match_en.yaml"])
match_config_de = testdata.load(["meetings", "test_match_de.yaml"])
match_config_fr = testdata.load(["meetings", "test_match_fr.yaml"])


@pytest.mark.parametrize("prefer, tests", [
    (c["prefer"], c["tests"]) for c in match_config_general
])
def test_match_general(prefer, tests):
    preferences.reset_options()
    testdata.apply_language_configurations("lang_en")
    _test_match(prefer, tests)


@pytest.mark.parametrize("prefer, tests", [
    (c["prefer"], c["tests"]) for c in match_config_en
])
def test_match_en(prefer, tests):
    preferences.reset_options()
    testdata.apply_language_configurations("lang_en")
    _test_match(prefer, tests)


@pytest.mark.parametrize("prefer, tests", [
    (c["prefer"], c["tests"]) for c in match_config_de
])
def test_match_de(prefer, tests):
    preferences.reset_options()
    testdata.apply_language_configurations("lang_de")
    _test_match(prefer, tests)


@pytest.mark.parametrize("prefer, tests", [
    (c["prefer"], c["tests"]) for c in match_config_fr
])
def test_match_fr(prefer, tests):
    preferences.reset_options()
    testdata.apply_language_configurations("lang_fr")
    _test_match(prefer, tests)


def _test_match(prefer, tests):
    """Compare cleaned dicts of loaded meetings with expected dicts."""
    for test in tests:
        date = test["date"]
        date = testdata.str_to_datetime(date)
        expected = test["expected"]
        if isinstance(prefer, dict):
            pref = TimePreference.from_dict(prefer)
        elif isinstance(prefer, str):
            pref = TimePreference.from_str(prefer)
        mdesc = pref.match(date)
        assert str(testdata.md2bool(mdesc)) == expected
