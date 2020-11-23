import pytest
import testdata

from meety import io

test_config = testdata.load(["meetings", "test_de.yaml"])


@pytest.mark.parametrize("input_dict, expected_dict", [
    (c["input"], c["expected"]) for c in test_config
])
def test_match(input_dict, expected_dict):
    """Compare cleaned dicts of loaded meetings with expected dicts."""
    testdata.apply_language_configurations("lang_de")
    assert io.process(input_dict) == expected_dict
