from abc import ABC
from typing import Dict, List, Union
from yada_token import Token

class Node(ABC):
    def token_literal(self) -> str:
        raise Exception("Method not implemented")

    def string(self) -> str:
        raise Exception("Method not implemented")

    def to_json(self) -> dict:
        raise Exception("Method not implemented")

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

    def to_json(self) -> dict:
        return {
            "node": self.__class__.__name__,
            "statements": [s.to_json() for s in self.statements],
        }

    def token_literal(self) -> str:
        if len(self.statements) > 0:
            return self.statements[0].token_literal()
        else:
            return ""

    def string(self) -> str:
        result = ""
        for s in self.statements:
            result += f"{s.string()}"
        return result
    
    def add_statement(self, stmt: Statement):
        self.statements.append(stmt)

class Identifier(Expression):
    token: Token
    value: str

    def __init__(self, token: Token, value: str):
        self.token = token
        self.value = value

    def to_json(self) -> dict:
        return {
            "node": self.__class__.__name__,
            "token": self.token.to_json(),
            "value": self.value,
        }
    
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

    def to_json(self) -> dict:
        return {
            "node": self.__class__.__name__,
            "token": self.token.to_json(),
            "name": self.name.to_json(),
            "value": self.value.to_json(),
        }
    
    def token_literal(self) -> str:
        return self.token.literal

    def string(self) -> str:
        return f"{self.token_literal()} {self.name.string()} = {self.value.string()};"


class ReturnStatement(Statement):
    token: Token
    return_value: Expression

    def __init__(self, token: Token, return_value: Expression):
        self.token = token
        self.return_value = return_value

    def to_json(self) -> dict:
        return {
            "node": self.__class__.__name__,
            "token": self.token.to_json(),
            "return_value": self.return_value.to_json(),
        }
    
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

    def to_json(self) -> dict:
        return {
            "node": self.__class__.__name__,
            "token": self.token.to_json(),
            "expression": self.expression.to_json(),
        }
    
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

    def to_json(self) -> dict:
        return {
            "node": self.__class__.__name__,
            "token": self.token.to_json(),
            "value": self.value,
        }
    
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

    def to_json(self) -> dict:
        return {
            "node": self.__class__.__name__,
            "token": self.token.to_json(),
            "value": self.value,
        }
    
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

    def to_json(self) -> dict:
        return {
            "node": self.__class__.__name__,
            "token": self.token.to_json(),
            "operator": self.operator,
            "right": self.right.to_json(),
        }

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

    def to_json(self) -> dict:
        return {
            "node": self.__class__.__name__,
            "token": self.token.to_json(),
            "left": self.left.to_json(),
            "operator": self.operator,
            "right": self.right.to_json(),
        }

    def token_literal(self) -> str:
        return self.token.literal

    def string(self) -> str:
        return f"({self.left.string()} {self.operator} {self.right.string()})"

class BlockStatement(Statement):
    token: Token
    statements: List[Statement]

    def __init__(self, token: Token, statements: List[Statement]):
        self.token = token
        self.statements = statements

    def to_json(self) -> dict:
        return {
            "node": self.__class__.__name__,
            "token": self.token.to_json(),
            "statements": [s.to_json() for s in self.statements],
        }

    def token_literal(self) -> str:
        return self.token.literal

    def string(self) -> str:
        result = ""
        for s in self.statements:
            result += s.string()
        return result

class IfExpression(Expression):
    token: Token
    condition: Expression
    consequence: BlockStatement
    alternative: BlockStatement | None

    def __init__(self, token: Token, condition: Expression, consequence: BlockStatement, alternative: BlockStatement):
        self.token = token
        self.condition = condition
        self.consequence = consequence
        self.alternative = alternative

    def to_json(self) -> dict:
        return {
            "node": self.__class__.__name__,
            "token": self.token.to_json(),
            "condition": self.condition.to_json(),
            "consequence": self.consequence.to_json(),
            "alternative": self.alternative.to_json() if self.alternative else None,
        }

    def token_literal(self) -> str:
        return self.token.literal

    def string(self) -> str:
        result = f"if {self.condition.string()} {self.consequence.string()}"
        if self.alternative:
            result += f" else {self.alternative.string()}"
        return result

class FunctionLiteral(Expression):
    token: Token
    parameters: List[Identifier]
    body: BlockStatement

    def __init__(self, token: Token, parameters: List[Identifier], body: BlockStatement):
        self.token = token
        self.parameters = parameters
        self.body = body

    def to_json(self) -> dict:
        return {
            "node": self.__class__.__name__,
            "token": self.token.to_json(),
            "parameters": [p.to_json() for p in self.parameters],
            "body": self.body.to_json(),
        }
    
    def token_literal(self) -> str:
        return self.token.literal

    def string(self) -> str:
        params = [p.string() for p in self.parameters]
        return f"{self.token_literal()}({', '.join(params)}) {{ {self.body.string()} }}"

class CallExpression(Expression):
    token: Token
    function: Expression # Identifier or Function Literal
    arguments: List[Expression]

    def __init__(self, token: Token, function: Expression, arguments: List[Expression]):
        self.token = token
        self.function = function
        self.arguments = arguments

    def to_json(self) -> dict:
        return {
            "node": self.__class__.__name__,
            "token": self.token.to_json(),
            "function": self.function.to_json(),
            "arguments": [a.to_json() for a in self.arguments],
        }

    def token_literal(self) -> str:
        return self.token.literal

    def string(self) -> str:
        args = [a.string() for a in self.arguments]
        return f"{self.function.string()}({', '.join(args)})"

class StringLiteral(Expression):
    token: Token
    value: str

    def __init__(self, token: Token, value: str):
        self.token = token
        self.value = value

    def to_json(self) -> dict:
        return {
            "node": self.__class__.__name__,
            "token": self.token.to_json(),
            "value": self.value,
        }
    
    def token_literal(self) -> str:
        return self.token.literal

    def string(self) -> str:
        return self.token.literal
    
class ArrayLiteral(Expression):
    token: Token
    elements: List[Expression]

    def __init__(self, token: Token, elements: List[Expression]):
        self.token = token
        self.elements = elements

    def to_json(self) -> dict:
        return {
            "node": self.__class__.__name__,
            "token": self.token.to_json(),
            "elements": [e.to_json() for e in self.elements],
        }
    
    def token_literal(self) -> str:
        return self.token.literal

    def string(self) -> str:
        els = [e.string() for e in self.elements]
        return f"[{', '.join(els)}]"
    
class IndexExpression(Expression):
    token: Token
    left: Expression
    index: Expression

    def __init__(self, token: Token, left: Expression, index: Expression):
        self.token = token
        self.left = left
        self.index = index

    def to_json(self) -> dict:
        return {
            "node": self.__class__.__name__,
            "token": self.token.to_json(),
            "left": self.left.to_json(),
            "index": self.index.to_json(),
        }

    def token_literal(self) -> str:
        return self.token.literal

    def string(self) -> str:
        return f"({self.left.string()}[{self.index.string()}])"


class HashLiteral(Expression):
    token: Token
    pairs: Dict[Expression, Expression]

    def __init__(self, token: Token, pairs: Dict[Expression, Expression]):
        self.token = token
        self.pairs = pairs

    def to_json(self) -> dict:
        # TODO: This
        return {
            "node": self.__class__.__name__,
            "token": self.token.to_json(),
            "pairs": None,
        }
    
    def token_literal(self) -> str:
        return self.token.literal

    def string(self) -> str:
        ps = list()
        for k, v in self.pairs.items():
            ps.append(f"{k.string()}:{v.string()}")
        return f"{{{', '.join(ps)}}}"