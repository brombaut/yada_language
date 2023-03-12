import json
import sys

from io import StringIO

from yada_ast import Program
from yada_lexer import Lexer
from yada_parser import Parser
from yada_token import TokenEnum
from yada_object import new_environment
from yada_evaluator import Eval

def Yada(input: str):
    l = Lexer(input)
    p = Parser(l)
    program: Program = p.parse_program()
    if len(p.errors) != 0:
        # TODO: Something
        pass
    # Print program ast style
    # print(program.string())
    
    temp_out = StringIO() # Create the in-memory "file"
    sys.stdout = temp_out # Replace default stdout (terminal) with our stream
    env = new_environment()
    evaluated = Eval(program, env)
    sys.stdout = sys.__stdout__ # Restore the original
    return {
        "program": program.to_json(),
        "evaluated": evaluated.inspect() if evaluated else evaluated,
        "environment": env.to_json(),
        "output": temp_out.getvalue(),
        "errors": p.errors,
    }


if __name__ == "__main__":
    test_input = """
    let x = 1;
    let y = 2;
    let add = fn(a, b) { return a + b };
    let result = add(x, y);
    puts(result);
    x;
    """
    output = Yada(test_input)
    # pp = pprint.PrettyPrinter(indent=4)
    # print(pp.pformat(json.dumps(output)))
    with open("sample.json", "w") as f:
        json.dump(output, f)
    # pprint.pprint(output)
    
