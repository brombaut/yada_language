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

        self.infix_parse_fns = dict()

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
        # TODO: Skipping the expressions until we get a semicolon
        while not self._curr_token_is(TokenEnum.SEMICOLON):
            self.next_token()
        return ast.LetStatement(let_token, let_ident, None)

    def _parse_return_statement(self) -> ast.ReturnStatement | None:
        return_token = self.curr_token
        self.next_token()
        # TODO: Skipping the expressions until we get a semicolon
        while not self._curr_token_is(TokenEnum.SEMICOLON):
            self.next_token()
        return ast.ReturnStatement(return_token, None)

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

    def _parse_prefix_expression(self) -> ast.Expression:
        token = self.curr_token
        operator = self.curr_token.literal
        self.next_token()
        right = self._parse_expression(ParsePrecedence.PREFIX)
        return ast.PrefixExpression(token, operator, right)

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

