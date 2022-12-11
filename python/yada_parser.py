from enum import Enum
from typing import Callable, Dict, List
from yada_lexer import Lexer
from yada_token import Token, TokenEnum
# from yada_ast import Program, Statement, LetStatement, Identifier, ReturnStatement, ExpressionStatement, Expression, IntegerLiteral
import yada_ast as ast

class ParsePrecedence(Enum):
    LOWEST = 0
    EQUALS = 1 # ==
    LESSGREATER = 2 # < or >
    SUM = 3 # +
    PRODUCT = 4 # *
    PREFIX = 5 # -X or !X
    CALL = 6 # foo(X)

PRECEDENCES = {
    TokenEnum.EQ: ParsePrecedence.EQUALS,
    TokenEnum.NOT_EQ: ParsePrecedence.EQUALS,
    TokenEnum.LT: ParsePrecedence.LESSGREATER,
    TokenEnum.GT: ParsePrecedence.LESSGREATER,
    TokenEnum.PLUS: ParsePrecedence.SUM,
    TokenEnum.MINUS: ParsePrecedence.SUM,
    TokenEnum.SLASH: ParsePrecedence.PRODUCT,
    TokenEnum.ASTERISK: ParsePrecedence.PRODUCT,
    TokenEnum.LPAREN: ParsePrecedence.CALL,
}

class Parser():
    lexer: Lexer
    errors: List[str]

    curr_token: Token
    peek_token: Token

    prefix_parse_fns: Dict[TokenEnum, Callable]
    infix_parse_fns: Dict[TokenEnum, Callable]


    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.curr_token, self.peek_token = None, None
        self.errors = []
        
        self.prefix_parse_fns = dict()
        self._register_prefix(TokenEnum.IDENT, self._parse_identifier)
        self._register_prefix(TokenEnum.INT, self._parse_integer_literal)
        self._register_prefix(TokenEnum.BANG, self._parse_prefix_expression)
        self._register_prefix(TokenEnum.MINUS, self._parse_prefix_expression)
        self._register_prefix(TokenEnum.TRUE, self._parse_boolean)
        self._register_prefix(TokenEnum.FALSE, self._parse_boolean)
        self._register_prefix(TokenEnum.LPAREN, self._parse_grouped_expression)
        self._register_prefix(TokenEnum.IF, self._parse_if_expression)
        self._register_prefix(TokenEnum.FUNCTION, self._parse_function_literal)

        self.infix_parse_fns = dict()
        self._register_infix(TokenEnum.PLUS, self._parse_infix_expression)
        self._register_infix(TokenEnum.MINUS, self._parse_infix_expression)
        self._register_infix(TokenEnum.SLASH, self._parse_infix_expression)
        self._register_infix(TokenEnum.ASTERISK, self._parse_infix_expression)
        self._register_infix(TokenEnum.EQ, self._parse_infix_expression)
        self._register_infix(TokenEnum.NOT_EQ, self._parse_infix_expression)
        self._register_infix(TokenEnum.LT, self._parse_infix_expression)
        self._register_infix(TokenEnum.GT, self._parse_infix_expression)
        self._register_infix(TokenEnum.LPAREN, self._parse_call_expression)

        self.next_token()
        self.next_token()

    def parse_program(self) -> ast.Program:
        program = ast.Program()
        while self.curr_token.type != TokenEnum.EOF:
            stmt = self._parse_statement()
            if stmt:
                program.add_statement(stmt)
            self.next_token()
        return program

    def next_token(self) -> None:
        self.curr_token = self.peek_token
        self.peek_token = self.lexer.next_token()

    def _parse_statement(self) -> ast.Statement | None:
        if self.curr_token.type == TokenEnum.LET:
            return self._parse_let_statement()
        elif self.curr_token.type == TokenEnum.RETURN:
            return self._parse_return_statement()
        else:
            return self._parse_expression_statement()

    def _parse_let_statement(self) -> ast.LetStatement | None:
        let_token = self.curr_token
        if not self._expect_peek(TokenEnum.IDENT):
            return None
        let_ident = ast.Identifier(self.curr_token, self.curr_token.literal)
        if not self._expect_peek(TokenEnum.ASSIGN):
            return None
        self.next_token()
        let_value = self._parse_expression(ParsePrecedence.LOWEST)
        if self._peek_token_is(TokenEnum.SEMICOLON):
            self.next_token()
        return ast.LetStatement(let_token, let_ident, let_value)

    def _parse_return_statement(self) -> ast.ReturnStatement | None:
        return_token = self.curr_token
        self.next_token()
        return_value = self._parse_expression(ParsePrecedence.LOWEST)
        if self._peek_token_is(TokenEnum.SEMICOLON):
            self.next_token()
        return ast.ReturnStatement(return_token, return_value)

    def _parse_expression_statement(self) -> ast.ExpressionStatement | None:
        expression_statement_token = self.curr_token
        expression_statement = self._parse_expression(ParsePrecedence.LOWEST)
        if self._peek_token_is(TokenEnum.SEMICOLON):
            self.next_token()
        return ast.ExpressionStatement(expression_statement_token, expression_statement)

    def _parse_expression(self, precendence: ParsePrecedence) -> ast.Expression | None:
        try:
            prefix = self.prefix_parse_fns[self.curr_token.type]
        except:
            self._no_prefix_parse_fn_error(self.curr_token.type)
            return None
        left_exp = prefix()

        while not self._peek_token_is(TokenEnum.SEMICOLON) and precendence.value < self._peek_precedence().value:
            try:
                infix = self.infix_parse_fns[self.peek_token.type]
            except:
                return left_exp
            self.next_token()
            left_exp = infix(left_exp)
        return left_exp

        return left_exp
    
    def _parse_identifier(self) -> ast.Identifier:
        return ast.Identifier(self.curr_token, self.curr_token.literal)

    def _parse_integer_literal(self) -> ast.Expression | None:
        integer_literal_token = self.curr_token
        try:
            value = int(integer_literal_token.literal)
        except:
            self.errors.append(f"could not parse {integer_literal_token.literal} as integer")
            return None
        return ast.IntegerLiteral(integer_literal_token, value)
    
    def _parse_boolean(self) -> ast.Expression | None:
        return ast.Boolean(self.curr_token, self._curr_token_is(TokenEnum.TRUE))

    def _parse_prefix_expression(self) -> ast.Expression:
        token = self.curr_token
        operator = self.curr_token.literal
        self.next_token()
        right = self._parse_expression(ParsePrecedence.PREFIX)
        return ast.PrefixExpression(token, operator, right)

    def _parse_infix_expression(self, left: ast.Expression) -> ast.Expression:
        token = self.curr_token
        operator = self.curr_token.literal
        precedence = self._cur_precedence()
        self.next_token()
        right = self._parse_expression(precedence)
        return ast.InfixExpression(token, left, operator, right)

    def _parse_grouped_expression(self) -> ast.Expression | None:
        self.next_token()
        exp = self._parse_expression(ParsePrecedence.LOWEST)
        if not self._expect_peek(TokenEnum.RPAREN):
            return None
        return exp
    
    def _parse_if_expression(self) -> ast.Expression | None:
        token = self.curr_token
        if not self._expect_peek(TokenEnum.LPAREN):
            return None
        self.next_token()
        condition = self._parse_expression(ParsePrecedence.LOWEST)
        if not self._expect_peek(TokenEnum.RPAREN):
            return None
        if not self._expect_peek(TokenEnum.LBRACE):
            return None
        consequence = self._parse_block_statement()
        alternative = None
        if self._peek_token_is(TokenEnum.ELSE):
            self.next_token()
            if not self._expect_peek(TokenEnum.LBRACE):
                return None
            alternative = self._parse_block_statement()
        return ast.IfExpression(token, condition, consequence, alternative)

    def _parse_block_statement(self) -> ast.BlockStatement:
        token = self.curr_token
        statements: List[ast.Statement] = []
        self.next_token()
        while not self._curr_token_is(TokenEnum.RBRACE) and not self._curr_token_is(TokenEnum.EOF):
            stmt = self._parse_statement()
            if stmt:
                statements.append(stmt)
            self.next_token()
        return ast.BlockStatement(token, statements)

    def _parse_function_literal(self) -> ast.Expression | None:
        token = self.curr_token
        if not self._expect_peek(TokenEnum.LPAREN):
            return None
        parameters = self._parse_function_parameters()
        if not self._expect_peek(TokenEnum.LBRACE):
            return None
        body = self._parse_block_statement()
        return ast.FunctionLiteral(token, parameters, body)

    def _parse_function_parameters(self) -> List[ast.Identifier]:
        identifiers: List[ast.Identifier] = list()
        if self._peek_token_is(TokenEnum.RPAREN):
            self.next_token()
            return identifiers
        self.next_token()
        ident = ast.Identifier(self.curr_token, self.curr_token.literal)
        identifiers.append(ident)
        while self._peek_token_is(TokenEnum.COMMA):
            self.next_token()
            self.next_token()
            ident = ast.Identifier(self.curr_token, self.curr_token.literal)
            identifiers.append(ident)
        if not self._expect_peek(TokenEnum.RPAREN):
            return None
        return identifiers

    def _parse_call_expression(self, function: ast.Expression) -> ast.Expression:
        token = self.curr_token
        arguments = self._parse_call_arguments()
        return ast.CallExpression(token, function, arguments)

    def _parse_call_arguments(self) -> List[ast.Expression]:
        args: List[ast.Expression] = list()
        if self._peek_token_is(TokenEnum.RPAREN):
            self.next_token()
            return args
        self.next_token()
        args.append(self._parse_expression(ParsePrecedence.LOWEST))
        while self._peek_token_is(TokenEnum.COMMA):
            self.next_token()
            self.next_token()
            args.append(self._parse_expression(ParsePrecedence.LOWEST))
        if not self._expect_peek(TokenEnum.RPAREN):
            return None
        return args

    def _curr_token_is(self, t: TokenEnum) -> bool:
        return self.curr_token.type == t

    def _peek_token_is(self, t: TokenEnum) -> bool:
        return self.peek_token.type == t

    def _expect_peek(self, t: TokenEnum) -> bool:
        if self._peek_token_is(t):
            self.next_token()
            return True
        else:
            self._peek_error(t)
            return False

    def _peek_error(self, t: TokenEnum):
        self.errors.append(f"Expected next token to be {t}, got {self.peek_token.type} instead")

    def _register_prefix(self, token_type: TokenEnum, fn: Callable):
        self.prefix_parse_fns[token_type] = fn

    def _register_infix(self, token_type: TokenEnum, fn: Callable):
        self.infix_parse_fns[token_type] = fn

    def _no_prefix_parse_fn_error(self, t: TokenEnum):
        self.errors.append(f"no prefix parse function found for {t}")

    def _peek_precedence(self) -> int:
        if self.peek_token.type in PRECEDENCES:
            return PRECEDENCES[self.peek_token.type]
        return ParsePrecedence.LOWEST

    def _cur_precedence(self) -> int:
        if self.curr_token.type in PRECEDENCES:
            return PRECEDENCES[self.curr_token.type]
        return ParsePrecedence.LOWEST