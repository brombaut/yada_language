from abc import ABC
from typing import Callable, Dict, List
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
    ARRAY_OBJ = "ARRAY"
    HASH_OBJ = "HASH"


class HashKey(object):
    type: ObjectTypeEnum
    value: int

    def __init__(self, type: ObjectTypeEnum, value: int):
        self.type = type
        self.value = value

    def __eq__(self, other):
        return type(other) == HashKey and \
            self.type == other.type and \
            self.value == other.value   

    def __ne__(self, other):
        return not (self == other)

class Hashable(ABC):
    def hash_key(self) -> HashKey:
        raise Exception("Method not implemented")

class Object(ABC):
    def type(self) -> str:
        raise Exception("Method not implemented")

    def inspect(self) -> str:
        raise Exception("Method not implemented")

class Integer(Object, Hashable):
    value: int

    def __init__(self, value: int):
        self.value = value
    
    def type(self) -> str:
        return ObjectTypeEnum.INTEGER_OBJ

    def inspect(self) -> str:
        return f"{self.value}"
    
    def hash_key(self) -> HashKey:
        return HashKey(self.type(), self.value)

class Boolean(Object, Hashable):
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
        
    def hash_key(self) -> HashKey:
        return HashKey(self.type(), 1 if self.value else 0)

class String(Object, Hashable):
    value: str

    def __init__(self, value: str):
        self.value = value
    
    def type(self) -> str:
        return ObjectTypeEnum.STRING_OBJ

    def inspect(self) -> str:
        return self.value
    
    def hash_key(self) -> HashKey:
        return HashKey(self.type(), hash(self.value))

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
    
class Array(Object):
    elements: List[Object]

    def __init__(self, els: List[Object]):
        self.elements = els

    def type(self) -> str:
        return ObjectTypeEnum.ARRAY_OBJ

    def inspect(self) -> str:
        els = [e.string() for e in self.elements]
        return f"[{', '.join(els)}]"
    
class HashPair():
    key: Object
    value: Object

    def __init__(self, key: Object, value: Object):
        self.key = key
        self.value = value

class Hash():
    pairs: Dict[HashKey, HashPair]

    def __init__(self, pairs: Dict[HashKey, HashPair]):
        self.pairs = pairs

    def type(self) -> str:
        return ObjectTypeEnum.HASH_OBJ

    def inspect(self) -> str:
        prs = [f"{p.key.inspect}: {p.value.inspect()}" for p in self.pairs]
        return f"{{{', '.join(prs)}}}"
