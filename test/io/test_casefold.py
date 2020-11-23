import pytest
import testdata

from meety import io

casefold_data = testdata.load(["io", "test_casefold.yaml"])


@pytest.mark.parametrize("input_data, expected_data", [
    (c["input"], c["expected"])
    for c in casefold_data
])
def test_casefold(input_data, expected_data):
    output = io.process_recursively(
        input_data,
        io._casefold_keys
    )
    assert output == expected_data
