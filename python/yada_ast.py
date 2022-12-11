from abc import ABC
from typing import List, Union
from yada_token import Token

class Node(ABC):
    def token_literal(self) -> str:
        raise Exception("Method not implements")

    def string(self) -> str:
        raise Exception("Method not implements")

class Statement(Node):
    pass

class Expression(Node):
    pass

class Program(Node):
    statements: List[Statement]

    def __init__(self, statements: Union[None, List[Statement]] = None):
        if not statements:
            self.statements = []
        else:
            self.statements = statements

    def token_literal(self) -> str:
        if len(self.statements) > 0:
            return self.statements[0].token_literal()
        else:
            return ""

    def string(self) -> str:
        result = ""
        for s in self.statements:
            result += s.string()
        return result
    
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

    def string(self) -> str:
        return self.value

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

    def string(self) -> str:
        return f"{self.token_literal()} {self.name.string()} = {self.value.string()};"


class ReturnStatement(Statement):
    token: Token
    return_value: Expression

    def __init__(self, token: Token, return_value: Expression):
        self.token = token
        self.value = return_value
    
    def token_literal(self) -> str:
        return self.token.literal

    def string(self) -> str:
        return_val_str = self.return_value.string() if self.return_value else ""
        return f"{self.token_literal()} {return_val_str};"

class ExpressionStatement(Statement):
    token: Token
    expression: Expression

    def __init__(self, token: Token, expression: Expression):
        self.token = token
        self.expression = expression
    
    def token_literal(self) -> str:
        return self.token.literal

    def string(self) -> str:
        return self.expression.string() if self.expression else ""

class IntegerLiteral(Expression):
    token: Token
    value: int

    def __init__(self, token: Token, value: int):
        self.token = token
        self.value = value
    
    def token_literal(self) -> str:
        return self.token.literal

    def string(self) -> str:
        return self.token.literal

class Boolean(Expression):
    token: Token
    value: bool

    def __init__(self, token: Token, value: bool):
        self.token = token
        self.value = value
    
    def token_literal(self) -> str:
        return self.token.literal

    def string(self) -> str:
        return self.token.literal

class PrefixExpression(Expression):
    token: Token
    operator: str
    right: Expression

    def __init__(self, token: Token, operator: str, right: Expression):
        self.token = token
        self.operator = operator
        self.right = right

    def token_literal(self) -> str:
        return self.token.literal

    def string(self) -> str:
        return f"({self.operator}{self.right.string()})"

class InfixExpression(Expression):
    token: Token
    left: Expression
    operator: str
    right: Expression

    def __init__(self, token: Token, left: Expression, operator: str, right: Expression):
        self.token = token
        self.left = left
        self.operator = operator
        self.right = right

    def token_literal(self) -> str:
        return self.token.literal

    def string(self) -> str:
        return f"({self.left.string()} {self.operator} {self.right.string()})"