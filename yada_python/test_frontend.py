import json
from yada_frontend import Yada

def load_test(file_name):
    with open(file_name) as f:
        return json.load(f)
    
def _test_results(expected, actual):
    assert expected["program"] == actual["program"], f"program ASTs do not match, got={actual['program']}"
    
    if expected["evaluated"]:
        assert expected["evaluated"] == actual["evaluated"], f'evaluated do not match, want={expected["evaluated"]}, got={actual["evaluated"]}'
    else:
        assert not actual["evaluated"], f'evaluated do not match, want={expected["evaluated"]}, got={actual["evaluated"]}'
    
    assert expected["environment"] == actual["environment"], f'environment do not match, want={expected["environment"]}, got={actual["environment"]}'
    
    if expected["output"]:
        assert expected["output"] == actual["output"], f'output do not match, want={expected["output"]}, got={actual["output"]}'
    else:
        assert not actual["output"], f'output do not match, want={expected["output"]}, got={actual["output"]}'
    
    assert expected["errors"] == actual["errors"], f'errors do not match, want={expected["errors"]}, got={actual["errors"]}'

def test_simple():
    t = load_test("frontend_tests/00_simple_test.json")
    expected = t["expected"]
    actual = Yada(t["input"])

    _test_results(expected, actual)
