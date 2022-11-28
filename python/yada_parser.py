from typing import List
from yada_lexer import Lexer
from yada_token import Token, TokenEnum
from yada_ast import Program, Statement, LetStatement, Identifier

class Parser():
    lexer: Lexer
    curr_token: Token
    peek_token: Token
    errors: List[str]

    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.curr_token, self.peek_token = None, None
        self.errors = []
        self.next_token()
        self.next_token()

    def parse_program(self) -> Program:
        program = Program()
        while self.curr_token.type != TokenEnum.EOF:
            stmt = self._parse_statement()
            if stmt:
                program.add_statement(stmt)
            self.next_token()
        return program

    def next_token(self) -> None:
        self.curr_token = self.peek_token
        self.peek_token = self.lexer.next_token()

    def _parse_statement(self) -> Statement | None:
        if self.curr_token.type == TokenEnum.LET:
            return self._parse_let_statement()
        else:
            return None

    def _parse_let_statement(self) -> LetStatement | None:
        let_token = self.curr_token
        if not self._expect_peek(TokenEnum.IDENT):
            return None
        let_ident = Identifier(self.curr_token, self.curr_token.literal)
        if not self._expect_peek(TokenEnum.ASSIGN):
            return None
        # TODO: Skipping the expressions until we get a semicolon
        while not self._curr_token_is(TokenEnum.SEMICOLON):
            self.next_token()
        return LetStatement(let_token, let_ident, None)

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
