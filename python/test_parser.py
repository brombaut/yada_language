
from yada_lexer import Lexer
from yada_parser import Parser
from yada_ast import Program, Statement, LetStatement, ReturnStatement, ExpressionStatement, Identifier, IntegerLiteral

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
    program: Program = parser.parse_program()
    check_parse_errors(parser)
    assert program is not None, "parse_program returned None"
    assert len(program.statements) == 3, f"program.statements does not contain 3 statements. got={len(program.statements)}"

    expected_identifiers = ["x", "y", "foobar"]
    for i, ei in enumerate(expected_identifiers):
        stmt = program.statements[i]
        assert stmt.token_literal() == "let", f"stmt.token_literal not 'let', got={stmt.token_literal()}"
        assert isinstance(stmt, LetStatement), f"stmt is not a LetStatement, got={type(stmt)}"
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
    program: Program = parser.parse_program()
    check_parse_errors(parser)

    assert len(program.statements) == 3, f"program.statements does not contain 3 statements. got={len(program.statements)}"
    for stmt in program.statements:
        assert isinstance(stmt, ReturnStatement), f"stmt is not a ReturnStatement, got={type(stmt)}"
        assert stmt.token_literal() == "return", f"return_statement.token_literal not 'return', got={stmt.token_literal()}"


def test_identifier_expression():
    input = """
    foobar;
    """
    lexer = Lexer(input)
    parser = Parser(lexer)
    program: Program = parser.parse_program()
    check_parse_errors(parser)

    assert len(program.statements) == 1, f"program.statements does not contain 1 statements. got={len(program.statements)}"
    stmt = program.statements[0]
    assert isinstance(stmt, ExpressionStatement), f"stmt is not a ExpressionStatement, got={type(stmt)}"
    ident = stmt.expression
    assert isinstance(ident, Identifier), f"expression_stmt.expression is not an Identifier, got={type(ident)}"
    assert ident.value == "foobar", f"ident.value not foobar, got={ident.value}"
    assert ident.token_literal() == "foobar", f"ident.token_literal() not foobar, got={ident.token_literal()}"


def test_integer_literal_expression():
    input = "5;"
    
    lexer = Lexer(input)
    parser = Parser(lexer)
    program: Program = parser.parse_program()
    check_parse_errors(parser)

    assert len(program.statements) == 1, f"program.statements does not contain 1 statements. got={len(program.statements)}"
    stmt = program.statements[0]
    assert isinstance(stmt, ExpressionStatement), f"stmt is not a ExpressionStatement, got={type(stmt)}"
    literal = stmt.expression
    assert isinstance(literal, IntegerLiteral), f"expression_stmt.expression is not an IntegerLiteral, got={type(literal)}"
    assert literal.value == 5, f"ident.value not 5, got={literal.value}"
    assert literal.token_literal() == "5", f"ident.token_literal() not 5, got={literal.token_literal()}"

