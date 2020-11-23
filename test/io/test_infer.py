import pytest
import testdata

from meety import io

infer_data = testdata.load(["io", "test_infer.yaml"])


@pytest.mark.parametrize("name, value, input_data, expected_data", [
    (c["name"], c["value"], c["input"], c["expected"])
    for c in infer_data
])
def test_infer(name, value, input_data, expected_data):
    action = io.actions.InferAction(name, value)
    output = io.process_recursively(
        input_data,
        lambda d, level:
        action.apply(d, level)
    )
    assert output == expected_data
