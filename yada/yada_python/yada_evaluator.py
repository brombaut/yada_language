import yada_ast as ast
import yada_object as obj
from typing import Callable, Dict, List

TRUE = obj.Boolean(True)
FALSE = obj.Boolean(False)
NULL = obj.Null()

def builtin_len(*args: List[obj.Object]) -> obj.Object:
    if len(args) != 1:
        return new_error(f"wrong number of arguments. got={len(args)}, want=1")
    arg = args[0]
    arg_type = type(arg)
    if arg_type == obj.Array:
        return obj.Integer(len(arg.elements))
    if arg_type == obj.String:
        return obj.Integer(len(arg.value))
    else:
        return new_error(f"argument to 'len' not supported, got={arg.type()}")

def builtin_first(*args: List[obj.Object]) -> obj.Object:
    if len(args) != 1:
        return new_error(f"wrong number of arguments. got={len(args)}, want=1")
    arg = args[0]
    arg_type = type(arg)
    if arg_type != obj.Array:
        return new_error(f"argument to 'first' must be ARRAY, got={arg.type()}")
    if len(arg.elements) > 0:
        return arg.elements[0]
    return None # TODO: Should this be NULL?

def builtin_last(*args: List[obj.Object]) -> obj.Object:
    if len(args) != 1:
        return new_error(f"wrong number of arguments. got={len(args)}, want=1")
    arg = args[0]
    arg_type = type(arg)
    if arg_type != obj.Array:
        return new_error(f"argument to 'last' must be ARRAY, got={arg.type()}")
    length = len(arg.elements)
    if length > 0:
        return arg.elements[length - 1]
    return None # TODO: Should this be NULL?


def builtin_rest(*args: List[obj.Object]) -> obj.Object:
    if len(args) != 1:
        return new_error(f"wrong number of arguments. got={len(args)}, want=1")
    arg = args[0]
    arg_type = type(arg)
    if arg_type != obj.Array:
        return new_error(f"argument to 'rest' must be ARRAY, got={arg.type()}")
    length = len(arg.elements)
    if length > 0:
        els = [e for e in arg.elements[1:]]
        return obj.Array(els)
    return None # TODO: Should this be NULL?

def builtin_push(*args: List[obj.Object]) -> obj.Object:
    if len(args) != 2:
        return new_error(f"wrong number of arguments. got={len(args)}, want=1")
    arr = args[0]
    arg_type = type(arr)
    if arg_type != obj.Array:
        return new_error(f"argument to 'push' must be ARRAY, got={arr.type()}")
    
    els = [e for e in arr.elements]
    els.append(args[1])
    return obj.Array(els)

def builtin_puts(*args: List[obj.Object]) -> obj.Object:
    for a in args:
        print(a.inspect())
    return NULL

BUILTINS: Dict[str, obj.Builtin] = {
    "len": obj.Builtin(builtin_len),
    "first": obj.Builtin(builtin_first),
    "last": obj.Builtin(builtin_last),
    "rest": obj.Builtin(builtin_rest),
    "push": obj.Builtin(builtin_push),
    "puts": obj.Builtin(builtin_puts),
}

def Eval(node: ast.Node, env: obj.Environment) -> obj.Object:
    node_type = type(node)
    # Statements
    if node_type == ast.Program:
        return eval_program(node, env)
    
    elif node_type == ast.ExpressionStatement:
        return Eval(node.expression, env)
    
    elif node_type == ast.BlockStatement:
        return eval_block_statement(node, env)
    
    elif node_type == ast.IfExpression:
        return eval_if_expression(node, env)
    
    elif node_type == ast.ReturnStatement:
        val = Eval(node.return_value, env)
        if (is_error(val)):
            return val
        return obj.ReturnValue(val)

    elif node_type == ast.LetStatement:
        val = Eval(node.value, env)
        if (is_error(val)):
            return val
        env.set(node.name.value, val)

    elif node_type == ast.FunctionLiteral:
        params = node.parameters
        body = node.body
        return obj.Function(params, body, env)

    elif node_type == ast.CallExpression:
        function = Eval(node.function, env)
        if (is_error(function)):
            return function
        args: List[obj.Object] = eval_expressions(node.arguments, env)
        if len(args) == 1 and is_error(args[0]):
            return args[0]
        return apply_function(function, args)

    elif node_type == ast.Identifier:
        return eval_identifier(node, env)
    
    elif node_type == ast.IntegerLiteral:
        return obj.Integer(node.value)
    
    elif node_type == ast.Boolean:
        return native_bool_to_boolean_object(node.value)

    elif node_type == ast.StringLiteral:
        return obj.String(node.value)
    
    elif node_type == ast.PrefixExpression:
        right = Eval(node.right, env)
        if (is_error(right)):
            return right
        return eval_prefix_expression(node.operator, right)
    
    elif node_type == ast.InfixExpression:
        left = Eval(node.left, env)
        if (is_error(left)):
            return left
        right = Eval(node.right, env)
        if (is_error(right)):
            return right
        return eval_infix_expression(node.operator, left, right)
    
    elif node_type == ast.ArrayLiteral:
        elements = eval_expressions(node.elements, env)
        if len(elements) == 1 and is_error(elements[0]):
            return elements[0]
        return obj.Array(elements)
    
    elif node_type == ast.IndexExpression:
        left = Eval(node.left, env)
        if (is_error(left)):
            return left
        index = Eval(node.index, env)
        if (is_error(index)):
            return index
        return eval_index_expression(left, index)
    
    elif node_type == ast.HashLiteral:
        return eval_hash_literal(node, env)

    return None

def eval_program(program: ast.Program, env: obj.Environment) -> obj.Object:
    result: obj.Object
    for statement in program.statements:
        result = Eval(statement, env)
        # result_type = type(result)
        if result:
            result_type = result.type()
            if result_type == obj.ObjectTypeEnum.RETURN_VALUE_OBJ:
                return result.value
            elif result_type == obj.ObjectTypeEnum.ERROR_OBJ:
                return result
    return result

# TODO: Is this used?
def eval_statements(stmts: List[ast.Statement], env: obj.Environment) -> obj.Object:
    result = obj.Object()
    for statement in stmts:
        result = Eval(statement, env)

        if type(result) == obj.ReturnValue:
            return result.value
    return result

def eval_block_statement(block: ast.BlockStatement, env: obj.Environment) -> obj.Object:
    result = obj.Object()
    for statement in block.statements:
        result = Eval(statement, env)
        if result:
            result_type = result.type()
            if result_type == obj.ObjectTypeEnum.RETURN_VALUE_OBJ or result_type == obj.ObjectTypeEnum.ERROR_OBJ:
                return result
    return result


def eval_expressions(exps: List[ast.Expression], env: obj.Environment) -> List[obj.Object]:
    result: List[obj.Object()] = []
    for e in exps:
        evaluated = Eval(e, env)
        if is_error(evaluated):
            return [obj.Object(evaluated)]
        result.append(evaluated)
    return result

def eval_prefix_expression(operator: str, right: obj.Object) -> obj.Object:
    if operator == "!":
        return eval_bang_operator_expression(right)
    elif operator == "-":
        return eval_minus_prefix_operator_expression(right)
    else:
        return new_error(f"unknown operator: {operator}{right.type()}")

def eval_infix_expression(operator: str, left: obj.Object, right: obj.Object) -> obj.Object:
    if left.type() == obj.ObjectTypeEnum.INTEGER_OBJ and right.type() == obj.ObjectTypeEnum.INTEGER_OBJ:
        return eval_integer_infix_expression(operator, left, right)
    elif left.type() == obj.ObjectTypeEnum.STRING_OBJ and right.type() == obj.ObjectTypeEnum.STRING_OBJ:
        return eval_string_infix_expression(operator, left, right)
    elif operator == "==":
        return native_bool_to_boolean_object(left == right)
    elif operator == "!=":
        return native_bool_to_boolean_object(left != right)
    elif left.type() != right.type():
        return new_error(f"type mismatch: {left.type()} {operator} {right.type()}")
    else:
        return new_error(f"unknown operator: {left.type()} {operator} {right.type()}")
    
def eval_index_expression(left: obj.Object, index: obj.Object) -> obj.Object:
    if left.type() == obj.ObjectTypeEnum.ARRAY_OBJ and index.type() == obj.ObjectTypeEnum.INTEGER_OBJ:
        return eval_array_index_expression(left, index)
    elif left.type() == obj.ObjectTypeEnum.HASH_OBJ:
        return eval_hash_index_expression(left, index)
    else:
        return new_error(f"index operator not supported: {left.type()}")

def eval_array_index_expression(left: obj.Array, index: obj.Integer) -> obj.Object:
    idx = index.value
    max_idx = len(left.elements) - 1
    if idx < 0 or idx > max_idx:
        return None # TODO: Should this return NULL?
    return left.elements[idx]

def eval_hash_literal(node: ast.HashLiteral, env: obj.Environment) -> obj.Object:
    pairs: Dict[obj.HashKey, obj.HashPair] = dict()
    for k_node, v_node in node.pairs.items():
        key = Eval(k_node, env)
        if is_error(key):
            return key
        if not isinstance(key, obj.Hashable):
            return new_error(f"unusable as hash key: {key.type()}")
        value = Eval(v_node, env)
        if is_error(value):
            return value
        hashed = key.hash_key()
        pairs[hashed] = obj.HashPair(key, value)
    return obj.Hash(pairs)

def eval_hash_index_expression(left: obj.Hash, index: obj.Integer) -> obj.Object:
    if not isinstance(index, obj.Hashable): 
        return new_error(f"unusable as hash key: {index.type()}")
    if index.hash_key() not in left.pairs:
        return None # TODO: Should this return NULL?
    pair: obj.HashPair = left.pairs[index.hash_key()]
    return pair.value

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
        return new_error(f"unknown operator: -{right.type()}")
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
        return new_error(f"unknown operator: {left.type()} {operator} {right.type()}")

def eval_string_infix_expression(operator: str, left: obj.String, right: obj.String) -> obj.Object:
    if operator != "+":
        return new_error(f"unknown operator: {left.type()} {operator} {right.type()}")
    left_val = left.value
    right_val = right.value
    return obj.String(left_val + right_val)

def eval_if_expression(ie: ast.IfExpression, env: obj.Environment) -> obj.Object:
    condition = Eval(ie.condition, env)
    if (is_error(condition)):
            return condition
    if is_truthy(condition):
        return Eval(ie.consequence, env)
    elif ie.alternative is not None:
        return Eval(ie.alternative, env)
    else:
        return None

def eval_identifier(node: ast.Identifier, env: obj.Environment) -> obj.Object:
    try:
        val = env.get(node.value)
        return val
    except: pass
    try:
        builtin = BUILTINS[node.value]
        return builtin
    except: pass
    return new_error(f"identifier not found: {node.value}")

def apply_function(fn: obj.Object, args: List[obj.Object]) -> obj.Object:
    fn_type = type(fn)
    if fn_type == obj.Function:
        extended_env = extend_function_env(fn, args)
        evaluated = Eval(fn.body, extended_env)
        return unwrap_return_value(evaluated)
    elif fn_type == obj.Builtin:
        return fn.fn(*args)
    else:
        return new_error(f"not a function: {fn.type()}")
        # raise Exception(f"not a function: {fn.type()}")
    
def extend_function_env(fn: obj.Object, args: List[obj.Object]) -> obj.Environment:
    env = obj.new_enclosed_environment(fn.env)
    for param_idx, param in enumerate(fn.parameters):
        env.set(param.value, args[param_idx])
    return env

def unwrap_return_value(m_obj: obj.Object) -> obj.Object:
    if type(m_obj) == obj.ReturnValue:
        return m_obj.value
    return m_obj

def native_bool_to_boolean_object(input: bool) -> obj.Boolean:
    if input:
        return TRUE
    return FALSE

def is_truthy(m_obj: obj.Object) -> bool:
    if m_obj == NULL:
        return False
    elif m_obj == TRUE:
        return True
    elif m_obj == FALSE:
        return False
    else:
        return True

def new_error(msg: str) -> obj.Error:
    return obj.Error(msg)

def is_error(m_obj: obj.Object) -> bool:
    if m_obj:
        return m_obj.type() == obj.ObjectTypeEnum.ERROR_OBJ
    return False