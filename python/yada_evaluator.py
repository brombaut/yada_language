import yada_ast as ast
import yada_object as obj
from typing import Callable, Dict, List

TRUE = obj.Boolean(True)
FALSE = obj.Boolean(False)
NULL = obj.Null

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
    elif node_type == ast.Boolean:
        return native_bool_to_boolean_object(node.value)
    return None

def eval_statements(stmts: List[ast.Statement]) -> obj.Object:
    result = obj.Object()
    for statement in stmts:
        result = Eval(statement)
    return result

def native_bool_to_boolean_object(input: bool) -> obj.Boolean:
    if input:
        return TRUE
    return FALSE