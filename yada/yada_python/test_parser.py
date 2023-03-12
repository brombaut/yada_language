
from typing import List
from yada_lexer import Lexer
from yada_parser import Parser
import yada_ast as ast
# from yada_ast import Program, Statement, LetStatement, ReturnStatement, ExpressionStatement, Identifier, IntegerLiteral, PrefixExpression

def check_parse_errors(p: Parser):
    errors = p.errors
    if len(errors) == 0:
        return
    for e in errors:
        print(f"\t{e}")
    assert len(errors) == 0, f"parser has {len(errors)} errors"

def test_let_statements():
    class LetStatementTest:
        def __init__(self, input, expected_identifier, expected_value):
            self.input: str = input
            self.expected_identifier: str = expected_identifier
            self.expected_value = expected_value
    
    let_statement_tests: List[LetStatementTest] = [
        LetStatementTest("let x = 5;", "x", 5),
        LetStatementTest("let y = true;", "y", True),
        LetStatementTest("let foobar = y;", "foobar", "y"),
    ]

    for lst in let_statement_tests:
        lexer = Lexer(lst.input)
        parser = Parser(lexer)
        program: ast.Program = parser.parse_program()
        check_parse_errors(parser)

        assert len(program.statements) == 1, f"program.statements does not contain 1 statements. got={len(program.statements)}"
        stmt = program.statements[0]
        if not _test_let_statement(stmt, lst.expected_identifier):
            return
        assert isinstance(stmt, ast.LetStatement), f"stmt is not a LetStatement, got={type(stmt)}"
        val = stmt.value
        if not _test_literal_expression(val, lst.expected_value):
            return

def test_return_statements():
    class ReturnStatementTest:
        def __init__(self, input, expected_value):
            self.input: str = input
            self.expected_value = expected_value
    
    return_statement_tests: List[ReturnStatementTest] = [
        ReturnStatementTest("return 5;", 5),
        ReturnStatementTest("return true;", True),
        ReturnStatementTest("return foobar;", "foobar"),
    ]

    for rst in return_statement_tests:
        lexer = Lexer(rst.input)
        parser = Parser(lexer)
        program: ast.Program = parser.parse_program()
        check_parse_errors(parser)

        assert len(program.statements) == 1, f"program.statements does not contain 1 statements. got={len(program.statements)}"
        ret_stmt = program.statements[0]
        assert isinstance(ret_stmt, ast.ReturnStatement), f"stmt is not a ReturnStatement, got={type(ret_stmt)}"
        assert ret_stmt.token_literal() == "return", f"return_statement.token_literal not 'return', got={ret_stmt.token_literal()}"
        if not _test_literal_expression(ret_stmt.return_value, rst.expected_value):
            return


def test_identifier_expression():
    input = """
    foobar;
    """
    lexer = Lexer(input)
    parser = Parser(lexer)
    program: ast.Program = parser.parse_program()
    check_parse_errors(parser)

    assert len(program.statements) == 1, f"program.statements does not contain 1 statements. got={len(program.statements)}"
    stmt = program.statements[0]
    assert isinstance(stmt, ast.ExpressionStatement), f"stmt is not a ExpressionStatement, got={type(stmt)}"
    ident = stmt.expression
    assert isinstance(ident, ast.Identifier), f"expression_stmt.expression is not an Identifier, got={type(ident)}"
    assert ident.value == "foobar", f"ident.value not foobar, got={ident.value}"
    assert ident.token_literal() == "foobar", f"ident.token_literal() not foobar, got={ident.token_literal()}"


def test_integer_literal_expression():
    input = "5;"
    
    lexer = Lexer(input)
    parser = Parser(lexer)
    program: ast.Program = parser.parse_program()
    check_parse_errors(parser)

    assert len(program.statements) == 1, f"program.statements does not contain 1 statements. got={len(program.statements)}"
    stmt = program.statements[0]
    assert isinstance(stmt, ast.ExpressionStatement), f"stmt is not a ExpressionStatement, got={type(stmt)}"
    literal = stmt.expression
    assert isinstance(literal, ast.IntegerLiteral), f"expression_stmt.expression is not an IntegerLiteral, got={type(literal)}"
    assert literal.value == 5, f"ident.value not 5, got={literal.value}"
    assert literal.token_literal() == "5", f"ident.token_literal() not 5, got={literal.token_literal()}"

def test_boolean_expression():
    input = "true;"
    
    lexer = Lexer(input)
    parser = Parser(lexer)
    program: ast.Program = parser.parse_program()
    check_parse_errors(parser)

    assert len(program.statements) == 1, f"program.statements does not contain 1 statements. got={len(program.statements)}"
    stmt = program.statements[0]
    assert isinstance(stmt, ast.ExpressionStatement), f"stmt is not a ExpressionStatement, got={type(stmt)}"
    literal = stmt.expression
    assert isinstance(literal, ast.Boolean), f"expression_stmt.expression is not a Boolean, got={type(literal)}"
    assert literal.value == True, f"ident.value not true, got={literal.value}"
    assert literal.token_literal() == "true", f"ident.token_literal() not true, got={literal.token_literal()}"

def test_string_literal_expression():
    input = '"hello world";'
    
    lexer = Lexer(input)
    parser = Parser(lexer)
    program: ast.Program = parser.parse_program()
    check_parse_errors(parser)

    assert len(program.statements) == 1, f"program.statements does not contain 1 statements. got={len(program.statements)}"
    stmt = program.statements[0]
    assert isinstance(stmt, ast.ExpressionStatement), f"stmt is not a ExpressionStatement, got={type(stmt)}"
    literal = stmt.expression
    assert isinstance(literal, ast.StringLiteral), f"expression_stmt.expression is not a StringLiteral, got={type(literal)}"
    assert literal.value == "hello world", f'ident.value not "hello world", got={literal.value}'


def test_parsing_prefix_expressions():
    class PrefixTest:
        def __init__(self, input, operator, integer_value):
            self.input: str = input
            self.operator: str = operator
            self.integer_value: int = integer_value
    
    prefix_tests: List[PrefixTest] = [
        PrefixTest("!5;", "!", 5),
        PrefixTest("-15;", "-", 15),
        PrefixTest("!true;", "!", True),
        PrefixTest("!false;", "!", False),
    ]

    for pt in prefix_tests:
        lexer = Lexer(pt.input)
        parser = Parser(lexer)
        program: ast.Program = parser.parse_program()
        check_parse_errors(parser)

        assert len(program.statements) == 1, f"program.statements does not contain 1 statements. got={len(program.statements)}"
        stmt = program.statements[0]
        assert isinstance(stmt, ast.ExpressionStatement), f"stmt is not a ExpressionStatement, got={type(stmt)}"
        exp = stmt.expression
        assert isinstance(exp, ast.PrefixExpression), f"expression_stmt.expression is not a PrefixExpression, got={type(exp)}"
        assert exp.operator == pt.operator, f"exp.operator is not {pt.operator}. got={exp.operator}"
        _test_literal_expression(exp.right, pt.integer_value)

def test_parsing_infix_expressions():
    class InfixTest:
        def __init__(self, input, left_value, operator, right_value):
            self.input: str = input
            self.left_value: int | bool = left_value
            self.operator: str = operator
            self.right_value: int | bool  = right_value

    infix_tests: List[InfixTest] = [
        InfixTest("5 + 5;", 5, "+", 5),
        InfixTest("5 - 5;", 5, "-", 5),
        InfixTest("5 * 5;", 5, "*", 5),
        InfixTest("5 / 5;", 5, "/", 5),
        InfixTest("5 > 5;", 5, ">", 5),
        InfixTest("5 < 5;", 5, "<", 5),
        InfixTest("5 == 5;", 5, "==", 5),
        InfixTest("5 != 5;", 5, "!=", 5),
        InfixTest("true == true;", True, "==", True),
        InfixTest("true != false;", True, "!=", False),
        InfixTest("false == false;", False, "==", False),
    ]

    for it in infix_tests:
        lexer = Lexer(it.input)
        parser = Parser(lexer)
        program: ast.Program = parser.parse_program()
        check_parse_errors(parser)

        assert len(program.statements) == 1, f"program.statements does not contain 1 statements. got={len(program.statements)}"
        stmt = program.statements[0]
        assert isinstance(stmt, ast.ExpressionStatement), f"stmt is not a ExpressionStatement, got={type(stmt)}"
        exp = stmt.expression

        if not _test_infix_expression(exp, it.left_value, it.operator,it.right_value):
            return

def test_operator_precedence_parsing():
    class OperatorPrecedenceTest():
        def __init__(self, input, expected):
            self.input: str = input
            self.expected: str = expected

    operator_precedence_tests: List[OperatorPrecedenceTest] = [
        OperatorPrecedenceTest("-a * b", "((-a) * b)"),
        OperatorPrecedenceTest("!-a", "(!(-a))"),
        OperatorPrecedenceTest("a + b + c", "((a + b) + c)"),
        OperatorPrecedenceTest("a + b - c", "((a + b) - c)"),
        OperatorPrecedenceTest("a * b * c", "((a * b) * c)"),
        OperatorPrecedenceTest("a * b / c", "((a * b) / c)"),
        OperatorPrecedenceTest("a + b / c", "(a + (b / c))"),
        OperatorPrecedenceTest("a + b * c + d / e - f", "(((a + (b * c)) + (d / e)) - f)"),
        OperatorPrecedenceTest("3 + 4; -5 * 5", "(3 + 4)((-5) * 5)"),
        OperatorPrecedenceTest("5 > 4 == 3 < 4", "((5 > 4) == (3 < 4))"),
        OperatorPrecedenceTest("5 < 4 != 3 > 4", "((5 < 4) != (3 > 4))"),
        OperatorPrecedenceTest("3 + 4 * 5 == 3 * 1 + 4 * 5", "((3 + (4 * 5)) == ((3 * 1) + (4 * 5)))"),
        OperatorPrecedenceTest("true", "true"),
        OperatorPrecedenceTest("false", "false"),
        OperatorPrecedenceTest("3 > 5 == false", "((3 > 5) == false)"),
        OperatorPrecedenceTest("3 < 5 == true", "((3 < 5) == true)"),
        OperatorPrecedenceTest("1 + (2 + 3) + 4", "((1 + (2 + 3)) + 4)"),
        OperatorPrecedenceTest("(5 + 5) * 2", "((5 + 5) * 2)"),
        OperatorPrecedenceTest("2 / (5 + 5)", "(2 / (5 + 5))"),
        OperatorPrecedenceTest("-(5 + 5)", "(-(5 + 5))"),
        OperatorPrecedenceTest("!(true == true)", "(!(true == true))"),
        OperatorPrecedenceTest("a + add(b * c) + d", "((a + add((b * c))) + d)"),
        OperatorPrecedenceTest("add(a, b, 1, 2 * 3, 4 + 5, add(6, 7 * 8))", "add(a, b, 1, (2 * 3), (4 + 5), add(6, (7 * 8)))"),
        OperatorPrecedenceTest("add(a + b + c * d / f + g)", "add((((a + b) + ((c * d) / f)) + g))"),
        OperatorPrecedenceTest(
            "a * [1, 2, 3, 4][b * c] * d",
            "((a * ([1, 2, 3, 4][(b * c)])) * d)"
        ),
        OperatorPrecedenceTest(
            "add(a * b[2], b[1], 2 * [1, 2][1])",
            "add((a * (b[2])), (b[1]), (2 * ([1, 2][1])))"
        )
    ]

    for opt in operator_precedence_tests:
        lexer = Lexer(opt.input)
        parser = Parser(lexer)
        program: ast.Program = parser.parse_program()
        check_parse_errors(parser)

        actual = program.string()
        assert actual == opt.expected, f"expected={opt.expected}, got={actual}"

def test_if_expression():
    input = "if (x < y) { x }"
    
    lexer = Lexer(input)
    parser = Parser(lexer)
    program: ast.Program = parser.parse_program()
    check_parse_errors(parser)

    assert len(program.statements) == 1, f"program.statements does not contain 1 statements. got={len(program.statements)}"
    stmt = program.statements[0]
    assert isinstance(stmt, ast.ExpressionStatement), f"stmt is not a ExpressionStatement, got={type(stmt)}"
    if_exp = stmt.expression
    assert isinstance(if_exp, ast.IfExpression), f"stmt.exp is not a IfExpression, got={type(if_exp)}"
    if not _test_infix_expression(if_exp.condition, "x", "<", "y"):
        return
    assert len(if_exp.consequence.statements) == 1, f"if_exp.consequence does not contain 1 statement. got={len(if_exp.consequence.statements)}"
    consequence = if_exp.consequence.statements[0]
    assert isinstance(consequence, ast.ExpressionStatement), f"consequence is not a ExpressionStatement, got={type(consequence)}"
    if not _test_identifier(consequence.expression, "x"):
        return
    assert not if_exp.alternative, f"if_exp.alternative was not None, got={if_exp.alternative}"

def test_if_else_expression():
    input = "if (x < y) { x } else { y }"
    
    lexer = Lexer(input)
    parser = Parser(lexer)
    program: ast.Program = parser.parse_program()
    check_parse_errors(parser)

    assert len(program.statements) == 1, f"program.statements does not contain 1 statements. got={len(program.statements)}"
    stmt = program.statements[0]
    assert isinstance(stmt, ast.ExpressionStatement), f"stmt is not a ExpressionStatement, got={type(stmt)}"
    if_else_exp = stmt.expression
    assert isinstance(if_else_exp, ast.IfExpression), f"stmt.exp is not a IfExpression, got={type(if_else_exp)}"
    if not _test_infix_expression(if_else_exp.condition, "x", "<", "y"):
        return
    assert len(if_else_exp.consequence.statements) == 1, f"if_exp.consequence does not contain 1 statement. got={len(if_else_exp.consequence.statements)}"
    consequence = if_else_exp.consequence.statements[0]
    assert isinstance(consequence, ast.ExpressionStatement), f"consequence is not a ExpressionStatement, got={type(consequence)}"
    if not _test_identifier(consequence.expression, "x"):
        return
    assert if_else_exp.alternative, f"if_else_exp.alternative was None, got={if_else_exp.alternative}"
    assert len(if_else_exp.alternative.statements) == 1, f"if_exp.alternative does not contain 1 statement. got={len(if_else_exp.consequence.statements)}"
    alternative = if_else_exp.alternative.statements[0]
    assert isinstance(alternative, ast.ExpressionStatement), f"alternative is not a ExpressionStatement, got={type(alternative)}"
    if not _test_identifier(alternative.expression, "y"):
        return

def test_function_literal_parsing():
    input = "fn(x, y) { x + y; }"
    lexer = Lexer(input)
    parser = Parser(lexer)
    program: ast.Program = parser.parse_program()
    check_parse_errors(parser)

    assert len(program.statements) == 1, f"program.statements does not contain 1 statements. got={len(program.statements)}"
    stmt = program.statements[0]
    assert isinstance(stmt, ast.ExpressionStatement), f"stmt is not a ExpressionStatement, got={type(stmt)}"
    function = stmt.expression
    assert isinstance(function, ast.FunctionLiteral), f"stmt.exp is not a FunctionLiteral, got={type(function)}"
    assert len(function.parameters) == 2, f"function literal parameters wrong. want 2. got={len(function.parameters)}"
    _test_literal_expression(function.parameters[0], "x")
    _test_literal_expression(function.parameters[1], "y")
    assert len(function.body.statements) == 1, f"function.body.statements has not 1 statement, got={len(function.body.statements)}"
    body_stmt = function.body.statements[0]
    assert isinstance(body_stmt, ast.ExpressionStatement), f"body_stmt is not a ExpressionStatement, got={type(body_stmt)}"
    _test_infix_expression(body_stmt.expression, "x", "+", "y")

def test_function_parameter_parsing():
    class FunctionParameterParsingTest():
        def __init__(self, input, expected_params):
            self.input: str = input
            self.expected_params: List[str] = expected_params

    function_parameter_parsing_tests: List[FunctionParameterParsingTest] = [
        FunctionParameterParsingTest("fn(){}", []),
        FunctionParameterParsingTest("fn(x){}", ["x"]),
        FunctionParameterParsingTest("fn(x, y, z){}", ["x", "y", "z"]),
    ]

    for t in function_parameter_parsing_tests:
        lexer = Lexer(t.input)
        parser = Parser(lexer)
        program: ast.Program = parser.parse_program()
        check_parse_errors(parser)

        assert len(program.statements) == 1, f"program.statements does not contain 1 statements. got={len(program.statements)}"
        stmt = program.statements[0]
        assert isinstance(stmt, ast.ExpressionStatement), f"stmt is not a ExpressionStatement, got={type(stmt)}"
        function = stmt.expression
        assert isinstance(function, ast.FunctionLiteral), f"stmt.exp is not a FunctionLiteral, got={type(function)}"
        assert len(function.parameters) == len(t.expected_params), f"function literal parameters wrong. want={len(t.expected_params)}. got={len(function.parameters)}"
        for i in range(len(t.expected_params)):
            _test_literal_expression(function.parameters[i], t.expected_params[i])

def test_call_expression():
    input = "add(1, 2 * 3, 4 + 5);"
    lexer = Lexer(input)
    parser = Parser(lexer)
    program: ast.Program = parser.parse_program()
    check_parse_errors(parser)

    assert len(program.statements) == 1, f"program.statements does not contain 1 statements. got={len(program.statements)}"
    stmt = program.statements[0]
    assert isinstance(stmt, ast.ExpressionStatement), f"stmt is not a ExpressionStatement, got={type(stmt)}"
    call_exp = stmt.expression
    assert isinstance(call_exp, ast.CallExpression), f"stmt.exp is not a CallExpression, got={type(call_exp)}"
    if not _test_identifier(call_exp.function, "add"):
        return
    assert len(call_exp.arguments) == 3, f"wrong length of arguments. got={len(call_exp.arguments)}"
    _test_literal_expression(call_exp.arguments[0], 1)
    _test_infix_expression(call_exp.arguments[1], 2, "*", 3)
    _test_infix_expression(call_exp.arguments[2], 4, "+", 5)

def test_parsing_array_literals():
    input = "[1, 2 * 2, 3 + 3]"
    lexer = Lexer(input)
    parser = Parser(lexer)
    program: ast.Program = parser.parse_program()
    check_parse_errors(parser)

    assert len(program.statements) == 1, f"program.statements does not contain 1 statements. got={len(program.statements)}"
    stmt = program.statements[0]
    assert isinstance(stmt, ast.ExpressionStatement), f"stmt is not a ExpressionStatement, got={type(stmt)}"
    array_exp = stmt.expression
    assert isinstance(array_exp, ast.ArrayLiteral), f"stmt.exp is not a ArrayLiteral, got={type(array_exp)}"
    assert len(array_exp.elements) == 3, f"len(array_exp.elements) not 3, got={len(array_exp.elements)}"
    _test_integer_literal(array_exp.elements[0], 1)
    _test_infix_expression(array_exp.elements[1], 2, "*", 2)
    _test_infix_expression(array_exp.elements[2], 3, "+", 3)

def test_parsing_index_expressions():
    input = "my_array[1 + 1]"
    lexer = Lexer(input)
    parser = Parser(lexer)
    program: ast.Program = parser.parse_program()
    check_parse_errors(parser)

    assert len(program.statements) == 1, f"program.statements does not contain 1 statements. got={len(program.statements)}"
    stmt = program.statements[0]
    assert isinstance(stmt, ast.ExpressionStatement), f"stmt is not a ExpressionStatement, got={type(stmt)}"
    index_exp = stmt.expression
    assert isinstance(index_exp, ast.IndexExpression), f"stmt.exp is not a IndexExpression, got={type(index_exp)}"
    _test_identifier(index_exp.left, "my_array")
    _test_infix_expression(index_exp.index, 1, "+", 1)

def test_parsing_hash_literal_string_keys():
    input = '{"one": 1, "two": 2, "three": 3}'
    lexer = Lexer(input)
    parser = Parser(lexer)
    program: ast.Program = parser.parse_program()
    check_parse_errors(parser)

    assert len(program.statements) == 1, f"program.statements does not contain 1 statements. got={len(program.statements)}"
    stmt = program.statements[0]
    assert isinstance(stmt, ast.ExpressionStatement), f"stmt is not a ExpressionStatement, got={type(stmt)}"
    hash_literal = stmt.expression
    assert isinstance(hash_literal, ast.HashLiteral), f"stmt.exp is not a HashLiteral, got={type(hash_literal)}"
    assert len(hash_literal.pairs) == 3, f"has.pairs has wrong length, got={len(hash_literal.pairs)}"
    expected = {
        "one": 1, 
        "two": 2,
        "three": 3,
    }
    for k, v in hash_literal.pairs.items():
        assert isinstance(k, ast.StringLiteral), f"key is not StringLiteral, got={type(k)}"
        expected_value = expected[k.string()]
        _test_integer_literal(v, expected_value)

def test_parsing_empty_hash_literal():
    input = "{}"
    lexer = Lexer(input)
    parser = Parser(lexer)
    program: ast.Program = parser.parse_program()
    check_parse_errors(parser)

    assert len(program.statements) == 1, f"program.statements does not contain 1 statements. got={len(program.statements)}"
    stmt = program.statements[0]
    assert isinstance(stmt, ast.ExpressionStatement), f"stmt is not a ExpressionStatement, got={type(stmt)}"
    hash_literal = stmt.expression
    assert isinstance(hash_literal, ast.HashLiteral), f"stmt.exp is not a HashLiteral, got={type(hash_literal)}"
    assert len(hash_literal.pairs) == 0, f"has.pairs has wrong length, got={len(hash_literal.pairs)}"

def test_parsing_hash_literal_expressions():
    input = '{"one": 0 + 1, "two": 10 - 8, "three": 15 / 5}'
    lexer = Lexer(input)
    parser = Parser(lexer)
    program: ast.Program = parser.parse_program()
    check_parse_errors(parser)

    assert len(program.statements) == 1, f"program.statements does not contain 1 statements. got={len(program.statements)}"
    stmt = program.statements[0]
    assert isinstance(stmt, ast.ExpressionStatement), f"stmt is not a ExpressionStatement, got={type(stmt)}"
    hash_literal = stmt.expression
    assert isinstance(hash_literal, ast.HashLiteral), f"stmt.exp is not a HashLiteral, got={type(hash_literal)}"
    assert len(hash_literal.pairs) == 3, f"has.pairs has wrong length, got={len(hash_literal.pairs)}"
    tests = {
        "one": lambda e: _test_infix_expression(e, 0, "+", 1),
        "two": lambda e: _test_infix_expression(e, 10, "-", 8),
        "three": lambda e: _test_infix_expression(e, 15, "/", 5),
    }
    for k, v in hash_literal.pairs.items():
        assert isinstance(k, ast.StringLiteral), f"key is not StringLiteral, got={type(k)}"
        assert k.string() in tests, f"No test function for key {k.string()}"
        test_func = tests[k.string()]
        test_func(v)

def _test_infix_expression(exp: ast.Expression, left, operator: str, right) -> bool:
    assert isinstance(exp, ast.InfixExpression), f"exp is not an InfixExpression, got={type(exp)}"
    assert _test_literal_expression(exp.left, left)
    assert exp.operator == operator, f"exp.operator is not {operator}, got={exp.operator}"
    assert _test_literal_expression(exp.right, right)
    return True

def _test_literal_expression(exp: ast.Expression, expected: str | int) -> bool:
    if type(expected) == int:
        return _test_integer_literal(exp, expected)
    elif type(expected) == str:
        return _test_identifier(exp, expected)
    elif type(expected) == bool:
        return _test_boolean(exp, expected)
    else:
        raise Exception(f"type of exp not handled. got={type(expected)}")

def _test_integer_literal(il: ast.Expression, value: int) -> bool:
    assert isinstance(il, ast.IntegerLiteral), f"il is not an IntegerLiteral, got={type(il)}"
    assert il.value == value, f"il.value not {value}. got={il.value}"
    assert il.token_literal() == f"{value}", f"il.token_literal() not {value}, got={il.token_literal()}"
    return True

def _test_identifier(ident: ast.Expression, value: str) -> bool:
    assert isinstance(ident, ast.Identifier), f"ident is not an Identifier, got={type(ident)}"
    assert ident.value == value, f"ident.value not {value}. got={ident.value}"
    assert ident.token_literal() == f"{value}", f"ident.token_literal() not {value}, got={ident.token_literal()}"
    return True

def _test_boolean(exp: ast.Expression, value: bool) -> bool:
    assert isinstance(exp, ast.Boolean), f"exp is not an Boolean, got={type(exp)}"
    assert exp.value == value, f"bo.value not {value}. got={exp.value}"
    assert exp.token_literal() == (f"true" if value else "false"), f"exp.token_literal() not {value}, got={exp.token_literal()}"
    return True

def _test_let_statement(stmt: ast.Statement, name: str):
    assert stmt.token_literal() == "let", f"stmt.token_literal not 'let', got={stmt.token_literal()}"
    assert isinstance(stmt, ast.LetStatement), f"stmt is not a LetStatement, got={type(stmt)}"
    assert stmt.name.value == name, f"let_stmt.name.value not {name}, got={stmt.name.value}"
    assert stmt.name.token_literal() == name, f"let_stmt.name.token_literal() not {name}, got={stmt.name.token_literal()}"

