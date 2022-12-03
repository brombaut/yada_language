from enum import Enum

class TokenEnum(Enum):
    ILLEGAL = "ILLEGAL"
    EOF = "EOF"
    
    # Identifiers + Literals
    IDENT = "IDENT"
    INT = "INT"
    
    # Operators
    ASSIGN = "="
    PLUS = "+"
    MINUS = "-"
    BANG = "!"
    ASTERISK = "*"
    SLASH = "/"
    EQ = "=="
    NOT_EQ = "!="

    LT = "<"
    GT = ">"
    
    # Delimiters
    COMMA = ","
    SEMICOLON = ";"

    LPAREN = "("
    RPAREN = ")"
    LBRACE = "{"
    RBRACE = "}"
    
    # Keywords
    FUNCTION = "FUNCTION"
    LET = "LET"
    TRUE = "TRUE"
    FALSE = "FALSE"
    IF = "IF"
    ELSE = "ELSE"
    RETURN = "RETURN"


class Token:
    type: TokenEnum
    literal: str

    def __init__(self, type: TokenEnum, literal: str):
        self.type = type
        self.literal = literal

    def __str__(self):
        return "{type: " + self.type.value + ", literal: " + self.literal + "}"


keywords = {
    "fn": TokenEnum.FUNCTION,
    "let": TokenEnum.LET,
    "true": TokenEnum.TRUE,
    "false": TokenEnum.FALSE,
    "if": TokenEnum.IF,
    "else": TokenEnum.ELSE,
    "return": TokenEnum.RETURN
}

def lookup_ident(ident: str) -> TokenEnum:
    if ident in keywords:
        return keywords[ident]
    return TokenEnum.IDENT