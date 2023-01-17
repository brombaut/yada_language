from abc import ABC

from enum import Enum

class ObjectTypeEnum(Enum):
    INTEGER_OBJ = "INTEGER"
    BOOLEAN_OBJ = "BOOLEAN"
    NULL_OBJ = "NULL"


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
