import pytest
import testdata

from meety import meetings
from meety.config import PartialConfig
from meety.loader import Loader

test_config = testdata.load(["test_loader.yaml"])


@pytest.mark.parametrize(
    "filename, further_filenames, expected, config",
    [
        (
            c["file"],
            c.get("further-files", []),
            c["expected"],
            c.get("config", {})
        ) for c in test_config
    ]
)
def test_loader(filename, further_filenames, expected, config):
    """Compare cleaned dicts of loaded meetings with expected dicts."""
    test_config = PartialConfig("test config", None, None)
    test_config._data = config
    test_config.apply()
    meetings.reset_options()
    meetings.set_options(test_config.meetings, "test_config")

    loader = Loader()
    _load_file(loader, filename)
    for f in further_filenames:
        _load_file(loader, f)
    assert [m.data for m in loader.meetings] == expected


def _load_file(loader, filename):
    loader.load_from_file(testdata.testpath(["data", filename]))
