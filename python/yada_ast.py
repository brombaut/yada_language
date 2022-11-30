from abc import ABC
from typing import List
from yada_token import Token

class Node(ABC):
    def token_literal() -> str:
        pass

class Statement(Node):
    pass

class Expression(Node):
    pass

class Program(Node):
    statements: List[Statement]

    def __init__(self):
        self.statements = []

    def token_literal(self) -> str:
        if len(self.statements) > 0:
            return self.statements[0].token_literal()
        else:
            return ""
    
    def add_statement(self, stmt: Statement):
        self.statements.append(stmt)

class Identifier(Expression):
    token: Token
    value: str

    def __init__(self, token: Token, value: str):
        self.token = token
        self.value = value
    
    def token_literal(self) -> str:
        return self.token.literal

class LetStatement(Statement):
    token: Token
    name: Identifier
    value: Expression

    def __init__(self, token: Token, name: Identifier, value: Expression):
        self.token = token
        self.name = name
        self.value = value
    
    def token_literal(self) -> str:
        return self.token.literal


class ReturnStatement(Statement):
    token: Token
    return_value: Expression

    def __init__(self, token: Token, return_value: Expression):
        self.token = token
        self.value = return_value
    
    def token_literal(self) -> str:
        return self.token.literal