
from yada_lexer import Lexer
from yada_parser import Parser
from yada_ast import Program, Statement, LetStatement

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
        assert stmt.token_literal() == "let", f"s.token_literal not 'let', got={stmt.token_literal()}"
        assert isinstance(stmt, LetStatement), f"s is not a LetStatement, got={type(stmt)}"
        assert stmt.name.value == ei, f"let_stmt.name.value not {ei}, got={stmt.name.value}"
        assert stmt.name.token_literal() == ei, f"let_stmt.name.token_literal() not {ei}, got={stmt.name.token_literal()}"


def check_parse_errors(p: Parser):
    errors = p.errors
    if len(errors) == 0:
        return
    for e in errors:
        print(f"\t{e}")
    assert len(errors) == 0, f"parser has {len(errors)} errors"