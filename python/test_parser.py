
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

def test_let_statement():
    input = """
    let x = 5;
    let y = 10;
    let foobar = 838383;
    """

    lexer = Lexer(input)
    parser = Parser(lexer)
    program: ast.Program = parser.parse_program()
    check_parse_errors(parser)
    assert program is not None, "parse_program returned None"
    assert len(program.statements) == 3, f"program.statements does not contain 3 statements. got={len(program.statements)}"

    expected_identifiers = ["x", "y", "foobar"]
    for i, ei in enumerate(expected_identifiers):
        stmt = program.statements[i]
        assert stmt.token_literal() == "let", f"stmt.token_literal not 'let', got={stmt.token_literal()}"
        assert isinstance(stmt, ast.LetStatement), f"stmt is not a LetStatement, got={type(stmt)}"
        assert stmt.name.value == ei, f"let_stmt.name.value not {ei}, got={stmt.name.value}"
        assert stmt.name.token_literal() == ei, f"let_stmt.name.token_literal() not {ei}, got={stmt.name.token_literal()}"


def test_return_statement():
    input = """
    return 5;
    return 10;
    return 993322;
    """

    lexer = Lexer(input)
    parser = Parser(lexer)
    program: ast.Program = parser.parse_program()
    check_parse_errors(parser)

    assert len(program.statements) == 3, f"program.statements does not contain 3 statements. got={len(program.statements)}"
    for stmt in program.statements:
        assert isinstance(stmt, ast.ReturnStatement), f"stmt is not a ReturnStatement, got={type(stmt)}"
        assert stmt.token_literal() == "return", f"return_statement.token_literal not 'return', got={stmt.token_literal()}"


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


def test_parsing_prefix_expressions():
    class PrefixTest:
        def __init__(self, input, operator, integer_value):
            self.input: str = input
            self.operator: str = operator
            self.integer_value: int = integer_value
    
    prefix_tests: List[PrefixTest] = [
        PrefixTest("!5;", "!", 5),
        PrefixTest("-15;", "-", 15)
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
        _test_integer_literal(exp.right, pt.integer_value)

def test_parsing_infix_expressions():
    class InfixTest:
        def __init__(self, input, left_value, operator, right_value):
            self.input: str = input
            self.left_value: int = left_value
            self.operator: str = operator
            self.right_value: int = right_value

    infix_tests: List[InfixTest] = [
        InfixTest("5 + 5;", 5, "+", 5),
        InfixTest("5 - 5;", 5, "-", 5),
        InfixTest("5 * 5;", 5, "*", 5),
        InfixTest("5 / 5;", 5, "/", 5),
        InfixTest("5 > 5;", 5, ">", 5),
        InfixTest("5 < 5;", 5, "<", 5),
        InfixTest("5 == 5;", 5, "==", 5),
        InfixTest("5 != 5;", 5, "!=", 5),
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
        assert isinstance(exp, ast.InfixExpression), f"expression_stmt.expression is not a InfixExpression, got={type(exp)}"
        _test_integer_literal(exp.left, it.left_value)
        assert exp.operator == it.operator, f"exp.operator is not {it.operator}. got={exp.operator}"
        _test_integer_literal(exp.right, it.right_value)

def _test_integer_literal(il: ast.Expression, value: int) -> bool:
    assert isinstance(il, ast.IntegerLiteral), f"il is not an IntegerLiteral, got={type(il)}"
    assert il.value == value, f"il.value not {value}. got={il.value}"
    assert il.token_literal() == f"{value}", f"il.token_literal() not {value}, got={il.token_literal()}"

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
    ]

    for opt in operator_precedence_tests:
        lexer = Lexer(opt.input)
        parser = Parser(lexer)
        program: ast.Program = parser.parse_program()
        check_parse_errors(parser)

        actual = program.string()
        assert actual == opt.expected, f"expected={opt.expected}, got={actual}"
