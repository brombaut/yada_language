import os

from yada_lexer import Lexer
from yada_token import TokenEnum

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
    while True:
        print(PROMPT, end=" ")
        line = input()
        if not line:
            return
        l = Lexer(line)
        tok = l.next_token()
        while tok.type != TokenEnum.EOF:
            print(tok)
            tok = l.next_token()
        

if __name__ == "__main__":
    main()