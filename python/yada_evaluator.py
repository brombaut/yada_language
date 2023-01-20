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
    elif node_type == ast.PrefixExpression:
        right = Eval(node.right)
        return eval_prefix_expression(node.operator, right)
    elif node_type == ast.InfixExpression:
        left = Eval(node.left)
        right = Eval(node.right)
        return eval_infix_expression(node.operator, left, right)
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

def eval_prefix_expression(operator: str, right: obj.Object) -> obj.Object:
    if operator == "!":
        return eval_bang_operator_expression(right)
    elif operator == "-":
        return eval_minus_prefix_operator_expression(right)
    else:
        return NULL

def eval_infix_expression(operator: str, left: obj.Object, right: obj.Object) -> obj.Object:
    if left.type() == obj.ObjectTypeEnum.INTEGER_OBJ and right.type() == obj.ObjectTypeEnum.INTEGER_OBJ:
        return eval_integer_infix_expression(operator, left, right)
    elif operator == "==":
        return native_bool_to_boolean_object(left == right)
    elif operator == "!=":
        return native_bool_to_boolean_object(left != right)
    else:
        return NULL
    
def eval_bang_operator_expression(right: obj.Object) -> obj.Object:
    if right == TRUE:
        return FALSE
    elif right == FALSE:
        return TRUE
    elif right == NULL:
        return TRUE
    else:
        return FALSE

def eval_minus_prefix_operator_expression(right: obj.Object) -> obj.Object:
    if right.type() != obj.ObjectTypeEnum.INTEGER_OBJ:
        return NULL
    value = right.value
    return obj.Integer(-value)

def eval_integer_infix_expression(operator: str, left: obj.Integer, right: obj.Integer) -> obj.Object:
    left_val = left.value
    right_val = right.value
    if operator == "+":
        return obj.Integer(left_val + right_val)
    elif operator == "-":
        return obj.Integer(left_val - right_val)
    elif operator == "*":
        return obj.Integer(left_val * right_val)
    elif operator == "/":
        return obj.Integer(left_val / right_val)
    elif operator == "<":
        return native_bool_to_boolean_object(left_val < right_val)
    elif operator == ">":
        return native_bool_to_boolean_object(left_val > right_val)
    elif operator == "==":
        return native_bool_to_boolean_object(left_val == right_val)
    elif operator == "!=":
        return native_bool_to_boolean_object(left_val != right_val)
    else:
        return NULL