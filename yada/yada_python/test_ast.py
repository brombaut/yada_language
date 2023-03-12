from yada_ast import Program, LetStatement, Identifier
from yada_token import Token, TokenEnum

def test_string():
    # let myVar = anotherVar;
    program = Program(statements=[
        LetStatement(
            Token(TokenEnum.LET, "let"),
            Identifier(
                Token(TokenEnum.IDENT, "myVar"),
                "myVar"
            ),
            Identifier(
                Token(TokenEnum.IDENT, "anotherVar"),
                "anotherVar"
            ),
        )
    ])
    assert program.string() == "let myVar = anotherVar;", f"program.string() wrong, got={program.string()}"