from abc import ABC

from enum import Enum

class ObjectTypeEnum(Enum):
    INTEGER_OBJ = "INTEGER"
    BOOLEAN_OBJ = "BOOLEAN"
    NULL_OBJ = "NULL"
    RETURN_VALUE_OBJ = "RETURN_VALUE"
    ERROR_OBJ = "OBJ"


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

class Null(Object):
    value: bool

    def __init__(self, value: bool):
        self.value = value
    
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

    def __init__(self, store: dict[str, Object]):
        self.store = store
    
    def get(self, name: str) -> Object:
        if name not in self.store:
            raise "TODO"
        return self.store[name]

    def set(self, name: str, val: Object) -> Object:
        self.store[name] = val
        return val

def new_environment() -> Environment:
    return Environment(dict())