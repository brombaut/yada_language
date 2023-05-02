import os

from yada.yada_python.yada_lexer import Lexer
from yada.yada_python.yada_parser import Parser
from yada.yada_python.yada_token import TokenEnum
from yada.yada_python.yada_object import new_environment
from yada.yada_python.yada_evaluator import Eval

PROMPT = ">>"

def main():
    print("yada yada yada")
    print()
    print(f"Hello {os.getlogin()}! This is the Yada Programming Language!")
    print("Feel free to type in commands")
    print()
    print("yada yada yada")
    start()

def start():
    env = new_environment()
    while True:
        print(PROMPT, end=" ")
        line = input()
        if not line:
            return
        l = Lexer(line)
        p = Parser(l)
        program = p.parse_program()
        if len(p.errors) != 0:
            print_parser_errors(p.errors)
            continue
        # Print program ast style
        # print(program.string())
        evaluated = Eval(program, env)
        if evaluated:
            print(evaluated.inspect())
            print()

def print_parser_errors(errors):
    print("ERROR: Paring errors:")
    for e in errors:
        print(f"\t{e}")        

if __name__ == "__main__":
    main()