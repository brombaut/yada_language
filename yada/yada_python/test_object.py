from typing import Any, List
from yada_evaluator import Eval
from yada_lexer import Lexer
from yada_parser import Parser
import yada_object as obj

def test_string_hash():
    hello_1 = obj.String("Hello World")
    hello_2 = obj.String("Hello World")
    diff_1 = obj.String("My name is johnny")
    diff_2 = obj.String("My name is johnny")
    assert hello_1.hash_key() == hello_2.hash_key(), f"strings with same content have different hash keys"
    assert diff_1.hash_key() == diff_2.hash_key(), f"strings with same content have different hash keys"
    assert hello_1.hash_key() != diff_2.hash_key(), f"strings with different content have same hash keys"