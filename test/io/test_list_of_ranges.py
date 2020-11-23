import pytest
import testdata

from meety import io

synonym_data = testdata.load(["io", "test_list_of_ranges.yaml"])


@pytest.mark.parametrize("input_data, expected_data", [
    (c["input"], c["expected"])
    for c in synonym_data
])
def test_list_of_ranges(input_data, expected_data):
    testdata.apply_language_configurations("lang_en", "lang_de")
    output = io.datetime.prepare_list_of_ranges(input_data)
    assert output == expected_data
