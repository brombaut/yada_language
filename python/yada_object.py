from abc import ABC
from typing import Callable, List
import yada_ast as ast
from enum import Enum

class ObjectTypeEnum(Enum):
    INTEGER_OBJ = "INTEGER"
    BOOLEAN_OBJ = "BOOLEAN"
    NULL_OBJ = "NULL"
    RETURN_VALUE_OBJ = "RETURN_VALUE"
    ERROR_OBJ = "ERROR"
    FUNCTION_OBJ = "FUNCTION"
    STRING_OBJ = "STRING"
    BUILTIN_OBJ = "BUILTIN"


class Object(ABC):
    def type(self) -> str:
        raise Exception("Method not implements")

    def inspect(self) -> str:
        raise Exception("Method not implements")

class Integer(Object):
    value: int

    def __init__(self, value: int):
        self.value = value
    
    def type(self) -> str:
        return ObjectTypeEnum.INTEGER_OBJ

    def inspect(self) -> str:
        return f"{self.value}"

class Boolean(Object):
    value: bool

    def __init__(self, value: bool):
        self.value = value
    
    def type(self) -> str:
        return ObjectTypeEnum.BOOLEAN_OBJ

    def inspect(self) -> str:
        if self.value:
            return "true"
        else:
            return "false"

class String(Object):
    value: str

    def __init__(self, value: str):
        self.value = value
    
    def type(self) -> str:
        return ObjectTypeEnum.STRING_OBJ

    def inspect(self) -> str:
        return self.value

class Null(Object):

    def __init__(self):
        pass

    def type(self) -> str:
        return ObjectTypeEnum.NULL_OBJ

    def inspect(self) -> str:
        return "null"

class ReturnValue(Object):
    value: Object

    def __init__(self, value: Object):
        self.value = value

    def type(self) -> str:
        return ObjectTypeEnum.RETURN_VALUE_OBJ

    def inspect(self) -> str:
        return self.value.inspect()

class Error(Object):
    message: str

    def __init__(self, message: str):
        self.message = message

    def type(self) -> str:
        return ObjectTypeEnum.ERROR_OBJ

    def inspect(self) -> str:
        return f"ERROR: {self.message}"


class Environment():
    store: dict[str, Object]
    outer: any # : Environment

    def __init__(self, store: dict[str, Object], outer: any):
        self.store = store
        self.outer = outer
    
    def get(self, name: str) -> Object:
        if name in self.store:
            return self.store[name]
        elif self.outer:
            # Will raise if not there
            return self.outer.get(name)
        else:
            # No outer env
            raise "TODO"

    def set(self, name: str, val: Object) -> Object:
        self.store[name] = val
        return val

def new_enclosed_environment(outer: Environment) -> Environment:
    env = new_environment()
    env.outer = outer
    return env

def new_environment() -> Environment:
    store = dict()
    outer_env = None
    return Environment(store, outer_env)




class Function(Object):
    parameters: List[ast.Identifier]
    body: ast.BlockStatement
    env: Environment

    def __init__(self, parameters: List[ast.Identifier], body: ast.BlockStatement, env: Environment):
        self.parameters = parameters
        self.body = body
        self.env = env

    def type(self) -> str:
        return ObjectTypeEnum.FUNCTION_OBJ

    def inspect(self) -> str:
        params = [p.string for p in self.parameters]
        return f"fn({','.join(params)}) {{ \n{self.body.string()}\n}}"



class Builtin(Object):
    fn: Callable[..., Object]

    def __init__(self, fn: Callable[..., Object]):
        self.fn = fn

    def type(self) -> str:
        return ObjectTypeEnum.BUILTIN_OBJ

    def inspect(self) -> str:
        return "builtin function"