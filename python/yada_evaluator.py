import yada_ast as ast
import yada_object as obj
from typing import Callable, Dict, List


def Eval(node: ast.Node) -> obj.Object:
    node_type = type(node)
    # Statements
    if node_type == ast.Program:
        return eval_statements(node.statements)
    elif node_type == ast.ExpressionStatement:
        return Eval(node.expression)
    # Expressions
    elif node_type == ast.IntegerLiteral:
        return obj.Integer(node.value)
    return None

def eval_statements(stmts: List[ast.Statement]) -> obj.Object:
    result = obj.Object()
    for statement in stmts:
        result = Eval(statement)
    return result

