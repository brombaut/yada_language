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
        EvalIfElseExpressionTest("if (1) { 10 }", 10),
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

def test_return_statements():
    class EvalReturnStatementTest:
        def __init__(self, input, expected):
            self.input: str = input
            self.expected: int = expected
    tests: List[EvalReturnStatementTest] = [
        EvalReturnStatementTest("return 10", 10),
        EvalReturnStatementTest("return 10; 9;", 10),
        EvalReturnStatementTest("return 2 * 5; 9;", 10),
        EvalReturnStatementTest("9; return 2 * 5; 9;", 10),
        EvalReturnStatementTest("""
        if (10 > 1) {
            if (10 > 1) {
                return 10;
            }
            return 1;
        }
        """, 10),

    ]

    for t in tests:
        evaluated = _test_eval(t.input)
        _test_integer_object(evaluated, t.expected)


def test_error_handling():
    class EvalErrorHandlingTest:
        def __init__(self, input, expected):
            self.input: str = input
            self.expected: str = expected
    tests: List[EvalErrorHandlingTest] = [
        EvalErrorHandlingTest("5 + true;", "type mismatch: ObjectTypeEnum.INTEGER_OBJ + ObjectTypeEnum.BOOLEAN_OBJ"),
        EvalErrorHandlingTest("5 + true; 5;", "type mismatch: ObjectTypeEnum.INTEGER_OBJ + ObjectTypeEnum.BOOLEAN_OBJ"),
        EvalErrorHandlingTest("-true;", "unknown operator: -ObjectTypeEnum.BOOLEAN_OBJ"),
        EvalErrorHandlingTest("true + false;", "unknown operator: ObjectTypeEnum.BOOLEAN_OBJ + ObjectTypeEnum.BOOLEAN_OBJ"),
        EvalErrorHandlingTest("5; true + false; 5", "unknown operator: ObjectTypeEnum.BOOLEAN_OBJ + ObjectTypeEnum.BOOLEAN_OBJ"),
        EvalErrorHandlingTest("if (10 > 1) { true + false; }", "unknown operator: ObjectTypeEnum.BOOLEAN_OBJ + ObjectTypeEnum.BOOLEAN_OBJ"),
        EvalErrorHandlingTest("""
        if (10 > 1) {
            if (10 > 1) {
                return true + false;
            }
            return 1;
        }
        """, "unknown operator: ObjectTypeEnum.BOOLEAN_OBJ + ObjectTypeEnum.BOOLEAN_OBJ"),
        EvalErrorHandlingTest("foobar", "identifier not found: foobar"),
        EvalErrorHandlingTest('"Hello" - "World"', "unknown operator: ObjectTypeEnum.STRING_OBJ - ObjectTypeEnum.STRING_OBJ"),
    ]

    for t in tests:
        evaluated = _test_eval(t.input)
        assert type(evaluated) == obj.Error, f"No error object returned. got={type(evaluated)}"
        assert evaluated.message == t.expected, f"wrong error message. expected={t.expected}, got={evaluated.message}"

def test_let_statements():
    class EvalLetStatementTest:
        def __init__(self, input, expected):
            self.input: str = input
            self.expected: int = expected
    tests: List[EvalLetStatementTest] = [
        EvalLetStatementTest("let a = 5; a;", 5),
        EvalLetStatementTest("let a = 5 * 5; a;", 25),
        EvalLetStatementTest("let a = 5; let b = a; b;", 5),
        EvalLetStatementTest("let a = 5; let b = a; let c = a + b + 5; c;", 15),
    ]
    for t in tests:
        evaluated = _test_eval(t.input)
        _test_integer_object(evaluated, t.expected)


def test_function_object():
    input = "fn(x) { x + 2; };"

    evaluated = _test_eval(input)
    assert isinstance(evaluated, obj.Function), f"object is not Function. got={type(evaluated)}"
    assert len(evaluated.parameters) == 1, f"function has wrong parameters. Parameters={evaluated.parameters}"
    assert evaluated.parameters[0].string() == "x", f"parameter is not x. got={evaluated.parameters[0].string()}"
    expected_body = "(x + 2)"
    assert evaluated.body.string() == expected_body, f"body is not {expected_body}. got={evaluated.body.string()}"

def test_function_application():
    class EvalFunctionTest:
        def __init__(self, input, expected):
            self.input: str = input
            self.expected: int = expected
    tests: List[EvalFunctionTest] = [
        EvalFunctionTest("let identity = fn(x) { x; }; identity(5);", 5),
        EvalFunctionTest("let identity = fn(x) { return x; }; identity(5);", 5),
        EvalFunctionTest("let double = fn(x) { x * 2; }; double(5);", 10),
        EvalFunctionTest("let add = fn(x, y) { x + y; }; add(5, 5);", 10),
        EvalFunctionTest("let add = fn(x, y) { x + y; }; add(5 + 5, add(5, 5));", 20),
        EvalFunctionTest("fn(x) { x; }(5)", 5),
    ]
    for t in tests:
        evaluated = _test_eval(t.input)
        _test_integer_object(evaluated, t.expected)

def test_closures():
    input = """
        let newAdder = fn(x) {
            fn(y) { x + y };
        };
        let addTwo = newAdder(2);
        addTwo(2);
    """
    expected = 4
    evaluated = _test_eval(input)
    _test_integer_object(evaluated, expected)

def test_string_literal():
    input = '"Hello World!"'
    evaluated = _test_eval(input)
    assert isinstance(evaluated, obj.String), f"evaluated object is not String, got={type(evaluated)}"
    assert evaluated.value == 'Hello World!', f"String has wrong value, got={evaluated.value}"

def test_string_concatenation():
    input = '"Hello" + " " + "World!"'
    evaluated = _test_eval(input)
    assert isinstance(evaluated, obj.String), f"evaluated object is not String, got={type(evaluated)}"
    assert evaluated.value == 'Hello World!', f"String has wrong value, got={evaluated.value}"

def _test_eval(inp: str) -> obj.Object:
    lexer = Lexer(inp)
    parser = Parser(lexer)
    program: ast.Program = parser.parse_program()
    env: obj.Environment = obj.new_environment()
    return Eval(program, env)

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

