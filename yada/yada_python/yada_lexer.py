from yada.yada_python.yada_token import Token, TokenEnum, lookup_ident

class Lexer:
    inp: str
    position: int
    read_position: int
    char: str

    def __init__(self, inp: str):
        self.inp = inp
        self.read_position = 0
        self._read_char()

    def next_token(self) -> Token:
        tok: Token
        self._skip_whitespace()
        if self.char == '=':
            if self._peek_char() == "=":
                c = self.char
                self._read_char()
                literal = f"{c}{self.char}"
                tok = self._new_token(TokenEnum.EQ, literal)
            else:
                tok = self._new_token(TokenEnum.ASSIGN, self.char)
        
        elif self.char == '+':
            tok = self._new_token(TokenEnum.PLUS, self.char)
        
        elif self.char == '-':
            tok = self._new_token(TokenEnum.MINUS, self.char)
        
        elif self.char == '!':
            if self._peek_char() == "=":
                c = self.char
                self._read_char()
                literal = f"{c}{self.char}"
                tok = self._new_token(TokenEnum.NOT_EQ, literal)
            else:
                tok = self._new_token(TokenEnum.BANG, self.char)
        
        elif self.char == '/':
            tok = self._new_token(TokenEnum.SLASH, self.char)
        
        elif self.char == '*':
            tok = self._new_token(TokenEnum.ASTERISK, self.char)
        
        elif self.char == '<':
            tok = self._new_token(TokenEnum.LT, self.char)
        
        elif self.char == '>':
            tok = self._new_token(TokenEnum.GT, self.char)
        
        elif self.char == ';':
            tok = self._new_token(TokenEnum.SEMICOLON, self.char)

        elif self.char == ':':
            tok = self._new_token(TokenEnum.COLON, self.char)
        
        elif self.char == ',':
            tok = self._new_token(TokenEnum.COMMA, self.char)
        
        elif self.char == '(':
            tok = self._new_token(TokenEnum.LPAREN, self.char)
        
        elif self.char == ')':
            tok = self._new_token(TokenEnum.RPAREN, self.char)
        
        elif self.char == '{':
            tok = self._new_token(TokenEnum.LBRACE, self.char)
        
        elif self.char == '}':
            tok = self._new_token(TokenEnum.RBRACE, self.char)

        elif self.char == '[':
            tok = self._new_token(TokenEnum.LBRACKET, self.char)
        elif self.char == ']':
            tok = self._new_token(TokenEnum.RBRACKET, self.char)
        
        elif self.char == '"':
            tok = self._new_token(TokenEnum.STRING, self._read_string())
        elif not self.char:
            tok = self._new_token(TokenEnum.EOF, '')
        
        else:
            if self._is_letter(self.char):
                ident = self._read_identifier()
                tok = self._new_token(lookup_ident(ident), ident)
                # Early return necessary because we have already 
                # advanced our pointer the new new char
                return tok
            elif self._is_digit(self.char):
                tok = self._new_token(TokenEnum.INT, self._read_number())
                # Early return necessary because we have already 
                # advanced our pointer the new new char
                return tok
            else:
                tok = self._new_token(TokenEnum.ILLEGAL, self.char)
        self._read_char()
        return tok

    def _read_char(self) -> None:
        if self.read_position >= len(self.inp):
            self.char = None
        else:
            self.char = self.inp[self.read_position]
        self.position = self.read_position
        self.read_position += 1

    def _peek_char(self) -> str:
        if self.read_position >= len(self.inp):
            return None
        else:
            return self.inp[self.read_position]

    def _read_identifier(self) -> str:
        position = self.position
        while self._is_letter(self.char):
            self._read_char()
        return self.inp[position:self.position]

    def _is_letter(self, char: str) -> bool:
        return char and (
            ('a' <= char and char <= 'z') or
            ('A' <= char and char <= 'Z') or
            char == '_'
        )

    def _new_token(self, token_type: TokenEnum, char: str) -> Token:
        return Token(token_type, char)

    def _skip_whitespace(self) -> None:
        whitespace_chars = [' ', '\t', '\n', '\r']
        while self.char in whitespace_chars:
            self._read_char()

    def _read_number(self) -> str:
        position = self.position
        while self._is_digit(self.char):
            self._read_char()
        return self.inp[position:self.position]

    def _is_digit(self, char: str) -> bool:
        return char and ('0' <= char and char <= '9')

    def _read_string(self) -> str:
        position = self.position + 1
        self._read_char()
        while self.char and self.char != "\"":
            self._read_char()
        return self.inp[position:self.position]
