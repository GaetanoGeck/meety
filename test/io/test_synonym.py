import pytest
import testdata

from meety import io

synonym_data = testdata.load(["io", "test_synonym.yaml"])


@pytest.mark.parametrize("input_data, expected_data, target_level", [
    (c["input"], c["expected"], c.get("level"))
    for c in synonym_data
])
def test_synonym(input_data, expected_data, target_level):
    action = io.actions.SynonymAction("out", ["in1", "in2"])
    if target_level:
        action.set_conditions(target_level)
    output = io.process_recursively(
        input_data,
        lambda d, current_level:
        action.apply(d, current_level)
    )
    assert output == expected_data
