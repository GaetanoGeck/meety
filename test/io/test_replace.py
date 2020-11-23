import pytest
import testdata

from meety import io

replace_data = testdata.load(["io", "test_replace.yaml"])


@pytest.mark.parametrize("key, expression, substitute, input_data, expected", [
    (
        c["key"],
        c["expression"],
        c["substitute"],
        c["input"],
        c["expected"],
    )
    for c in replace_data
])
def test_replace(key, expression, substitute, input_data, expected):
    action = io.actions.ReplaceAction(key, expression, substitute)
    output = io.process_recursively(
        input_data,
        lambda d, current_level:
        action.apply(d, current_level)
    )
    assert output == expected
