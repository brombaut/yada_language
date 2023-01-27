from typing import List, Dict
import pytest

from yada_token import TokenEnum, Token
from yada_lexer import Lexer


def test_next_token():
    inp = """
    let five = 5;
    let ten = 10;
    let add = fn(x, y) {
        x + y;
    };
    let result = add(five, ten);
    !-/*5;
    5 < 10 > 5;

    if (5 < 10) {
        return true;
    } else {
        return false;
    }

    10 == 10;
    10 != 9;
    "foobar"
    "foo bar"
    """

    expected_tokens: List[Token] = [
        Token(TokenEnum.LET, "let"),
        Token(TokenEnum.IDENT, "five"),
        Token(TokenEnum.ASSIGN, "="),
        Token(TokenEnum.INT, "5"),
        Token(TokenEnum.SEMICOLON, ";"),
        Token(TokenEnum.LET, "let"),
        Token(TokenEnum.IDENT, "ten"),
        Token(TokenEnum.ASSIGN, "="),
        Token(TokenEnum.INT, "10"),
        Token(TokenEnum.SEMICOLON, ";"),
        Token(TokenEnum.LET, "let"),
        Token(TokenEnum.IDENT, "add"),
        Token(TokenEnum.ASSIGN, "="),
        Token(TokenEnum.FUNCTION, "fn"),
        Token(TokenEnum.LPAREN, "("),
        Token(TokenEnum.IDENT, "x"),
        Token(TokenEnum.COMMA, ","),
        Token(TokenEnum.IDENT, "y"),
        Token(TokenEnum.RPAREN, ")"),
        Token(TokenEnum.LBRACE, "{"),
        Token(TokenEnum.IDENT, "x"),
        Token(TokenEnum.PLUS, "+"),
        Token(TokenEnum.IDENT, "y"),
        Token(TokenEnum.SEMICOLON, ";"),
        Token(TokenEnum.RBRACE, "}"),
        Token(TokenEnum.SEMICOLON, ";"),
        Token(TokenEnum.LET, "let"),
        Token(TokenEnum.IDENT, "result"),
        Token(TokenEnum.ASSIGN, "="),
        Token(TokenEnum.IDENT, "add"),
        Token(TokenEnum.LPAREN, "("),
        Token(TokenEnum.IDENT, "five"),
        Token(TokenEnum.COMMA, ","),
        Token(TokenEnum.IDENT, "ten"),
        Token(TokenEnum.RPAREN, ")"),
        Token(TokenEnum.SEMICOLON, ";"),
        Token(TokenEnum.BANG, "!"),
        Token(TokenEnum.MINUS, "-"),
        Token(TokenEnum.SLASH, "/"),
        Token(TokenEnum.ASTERISK, "*"),
        Token(TokenEnum.INT, "5"),
        Token(TokenEnum.SEMICOLON, ";"),
        Token(TokenEnum.INT, "5"),
        Token(TokenEnum.LT, "<"),
        Token(TokenEnum.INT, "10"),
        Token(TokenEnum.GT, ">"),
        Token(TokenEnum.INT, "5"),
        Token(TokenEnum.SEMICOLON, ";"),
        
        Token(TokenEnum.IF, "if"),
        Token(TokenEnum.LPAREN, "("),
        Token(TokenEnum.INT, "5"),
        Token(TokenEnum.LT, "<"),
        Token(TokenEnum.INT, "10"),
        Token(TokenEnum.RPAREN, ")"),
        Token(TokenEnum.LBRACE, "{"),
        Token(TokenEnum.RETURN, "return"),
        Token(TokenEnum.TRUE, "true"),
        Token(TokenEnum.SEMICOLON, ";"),
        Token(TokenEnum.RBRACE, "}"),
        Token(TokenEnum.ELSE, "else"),
        Token(TokenEnum.LBRACE, "{"),
        Token(TokenEnum.RETURN, "return"),
        Token(TokenEnum.FALSE, "false"),
        Token(TokenEnum.SEMICOLON, ";"),
        Token(TokenEnum.RBRACE, "}"),

        Token(TokenEnum.INT, "10"),
        Token(TokenEnum.EQ, "=="),
        Token(TokenEnum.INT, "10"),
        Token(TokenEnum.SEMICOLON, ";"),

        Token(TokenEnum.INT, "10"),
        Token(TokenEnum.NOT_EQ, "!="),
        Token(TokenEnum.INT, "9"),
        Token(TokenEnum.SEMICOLON, ";"),

        Token(TokenEnum.STRING, "foobar"),
        Token(TokenEnum.STRING, "foo bar"),

        Token(TokenEnum.EOF, "")
    ]
    l = Lexer(inp)
    for t in expected_tokens:
        tok = l.next_token()
        # print(tok.type, t.type, tok.literal, t.literal)
        
        assert tok.type == t.type, "incorrect token type"
        assert tok.literal == t.literal, "incorrect literal"