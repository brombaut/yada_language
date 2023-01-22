from typing import Any, List
from yada_evaluator import Eval
from yada_lexer import Lexer
from yada_parser import Parser
import yada_object as obj
import yada_ast as ast



def test_eval_integer_expression():
    class EvalIntegerExpressionTest:
        def __init__(self, input, expected):
            self.input: str = input
            self.expected: int = expected
    eval_integer_expression_tests: List[EvalIntegerExpressionTest] = [
        EvalIntegerExpressionTest("5", 5),
        EvalIntegerExpressionTest("10", 10),
        EvalIntegerExpressionTest("-5", -5),
        EvalIntegerExpressionTest("-10", -10),
        EvalIntegerExpressionTest("5 + 5 + 5 + 5 - 10", 10),
        EvalIntegerExpressionTest("2 * 2 * 2 * 2 * 2", 32),
        EvalIntegerExpressionTest("-50 + 100 + -50", 0),
        EvalIntegerExpressionTest("5 * 2 + 10", 20),
        EvalIntegerExpressionTest("5 + 2 * 10", 25),
        EvalIntegerExpressionTest("20 + 2 * -10", 0),
        EvalIntegerExpressionTest("50 / 2 * 2 + 10", 60),
        EvalIntegerExpressionTest("2 * (5 + 10)", 30),
        EvalIntegerExpressionTest("3 * 3 * 3 + 10", 37),
        EvalIntegerExpressionTest("3 * (3 * 3) + 10", 37),
        EvalIntegerExpressionTest("(5 + 10 * 2 + 15 / 3) * 2 + -10", 50),
    ]

    for t in eval_integer_expression_tests:
        evaluated = _test_eval(t.input)
        _test_integer_object(evaluated, t.expected)

def test_eval_boolean_expression():
    class EvalBooleanExpressionTest:
        def __init__(self, input, expected):
            self.input: str = input
            self.expected: bool = expected
    eval_boolean_expression_tests: List[EvalBooleanExpressionTest] = [
        EvalBooleanExpressionTest("true", True),
        EvalBooleanExpressionTest("false", False),
        EvalBooleanExpressionTest("1 < 2", True),
        EvalBooleanExpressionTest("1 > 2", False),
        EvalBooleanExpressionTest("1 < 1", False),
        EvalBooleanExpressionTest("1 > 1", False),
        EvalBooleanExpressionTest("1 == 1", True),
        EvalBooleanExpressionTest("1 != 1", False),
        EvalBooleanExpressionTest("1 == 2", False),
        EvalBooleanExpressionTest("1 != 2", True),
        EvalBooleanExpressionTest("true == true", True),
        EvalBooleanExpressionTest("false == false", True),
        EvalBooleanExpressionTest("true == false", False),
        EvalBooleanExpressionTest("true != false", True),
        EvalBooleanExpressionTest("true == true", True),
        EvalBooleanExpressionTest("(1 < 2) == true", True),
        EvalBooleanExpressionTest("(1 < 2) == false", False),
        EvalBooleanExpressionTest("(1 > 2) == true", False),
        EvalBooleanExpressionTest("(1 > 2) == false", True),
    ]

    for t in eval_boolean_expression_tests:
        evaluated = _test_eval(t.input)
        _test_boolean_object(evaluated, t.expected)

def test_bang_operator():
    class EvalBangOperatorTest:
        def __init__(self, input, expected):
            self.input: str = input
            self.expected: bool = expected
    tests: List[EvalBangOperatorTest] = [
        EvalBangOperatorTest("!true", False),
        EvalBangOperatorTest("!false", True),
        EvalBangOperatorTest("!5", False),
        EvalBangOperatorTest("!!true", True),
        EvalBangOperatorTest("!!false", False),
        EvalBangOperatorTest("!!5", True),
    ]

    for t in tests:
        evaluated = _test_eval(t.input)
        _test_boolean_object(evaluated, t.expected)


def test_if_else_expressions():
    class EvalIfElseExpressionTest:
        def __init__(self, input, expected):
            self.input: str = input
            self.expected: Any = expected
    tests: List[EvalIfElseExpressionTest] = [
        EvalIfElseExpressionTest("if (true) { 10 }", 10),
        EvalIfElseExpressionTest("if (false) { 10 }", None),
        EvalIfElseExpressionTest("if (q) { 10 }", 10),
        EvalIfElseExpressionTest("if (1 < 2) { 10 }", 10),
        EvalIfElseExpressionTest("if (1 > 2) { 10 }", None),
        EvalIfElseExpressionTest("if (1 > 2) { 10 } else { 20 }", 20),
        EvalIfElseExpressionTest("if (1 < 2) { 10 } else { 20 }", 10),
    ]

    for t in tests:
        evaluated = _test_eval(t.input)
        if type(t.expected) == int:
            _test_integer_object(evaluated, t.expected)
        else:
            _test_null_object(evaluated)

def _test_eval(inp: str) -> obj.Object:
    lexer = Lexer(inp)
    parser = Parser(lexer)
    program: ast.Program = parser.parse_program()
    return Eval(program)

def _test_integer_object(actual_obj: obj.Object, expected: int) -> bool:
    assert isinstance(actual_obj, obj.Integer), f"actual_obj is not Integer, got={type(actual_obj)}"
    assert actual_obj.value == expected, f"actual_obj has wrong value. got={actual_obj.value}, want={expected}"
    return True

def _test_boolean_object(actual_obj: obj.Object, expected: bool) -> bool:
    assert isinstance(actual_obj, obj.Boolean), f"actual_obj is not Boolean, got={type(actual_obj)}"
    assert actual_obj.value == expected, f"actual_obj has wrong value. got={actual_obj.value}, want={expected}"
    return True

def _test_null_object(actual_obj: obj.Object) -> bool:
    assert actual_obj is None, f"actual_obj is not None, got={type(actual_obj)}"
    return True

