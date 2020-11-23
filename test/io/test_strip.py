import pytest
import testdata

from meety import io

strip_data = testdata.load(["io", "test_strip.yaml"])


@pytest.mark.parametrize("name, texts, input_data, expected_data", [
    (c["name"], c["texts"], c["input"], c["expected"])
    for c in strip_data
])
def test_strip(name, texts, input_data, expected_data):
    action = io.actions.StripAction(name, texts)
    output = io.process_recursively(
        input_data,
        lambda d, level:
        action.apply(d, level)
    )
    assert output == expected_data
