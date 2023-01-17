from abc import ABC

from enum import Enum

class ObjectTypeEnum(Enum):
    INTEGER_OBJ = "INTEGER"


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