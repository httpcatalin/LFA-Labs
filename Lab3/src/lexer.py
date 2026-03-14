from token import Token, TokenType

class Lexer:
    KEYWORDS = {
        'sin': TokenType.SIN,
        'cos': TokenType.COS,
        'tan': TokenType.TAN,
        'sqrt': TokenType.SQRT,
    }
    
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens = []
    
    def error(self, message):
        token = Token(TokenType.ERROR, message, self.line, self.column)
        self.tokens.append(token)
        return token
    
    def current_char(self):
        if self.pos >= len(self.text):
            return None
        return self.text[self.pos]
    
    def peek_char(self, offset=1):
        peek_pos = self.pos + offset
        if peek_pos >= len(self.text):
            return None
        return self.text[peek_pos]
    
    def advance(self):
        if self.pos < len(self.text):
            if self.text[self.pos] == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.pos += 1
    
    def skip_whitespace(self):
        while self.current_char() and self.current_char().isspace():
            self.advance()
    
    def skip_comment(self):
        if self.current_char() == '#':
            while self.current_char() and self.current_char() != '\n':
                self.advance()
            if self.current_char() == '\n':
                self.advance()
    
    def read_number(self):
        start_pos = self.pos
        start_col = self.column
        
        while self.current_char() and self.current_char().isdigit():
            self.advance()
        
        if self.current_char() == '.' and self.peek_char() and self.peek_char().isdigit():
            self.advance()
            while self.current_char() and self.current_char().isdigit():
                self.advance()
            value = float(self.text[start_pos:self.pos])
            return Token(TokenType.FLOAT, value, self.line, start_col)
        else:
            value = int(self.text[start_pos:self.pos])
            return Token(TokenType.INTEGER, value, self.line, start_col)
    
    def read_identifier(self):
        start_pos = self.pos
        start_col = self.column
        
        while self.current_char() and (self.current_char().isalnum() or self.current_char() == '_'):
            self.advance()
        
        identifier = self.text[start_pos:self.pos]
        
        if identifier in self.KEYWORDS:
            return Token(self.KEYWORDS[identifier], identifier, self.line, start_col)
        else:
            return Token(TokenType.IDENTIFIER, identifier, self.line, start_col)
    
    def tokenize(self):
        while self.pos < len(self.text):
            self.skip_whitespace()
            
            if self.current_char() is None:
                break
            
            if self.current_char() == '#':
                self.skip_comment()
                continue
            
            char = self.current_char()
            col = self.column
            
            if char.isdigit():
                self.tokens.append(self.read_number())
            elif char.isalpha() or char == '_':
                self.tokens.append(self.read_identifier())
            elif char == '+':
                self.tokens.append(Token(TokenType.PLUS, '+', self.line, col))
                self.advance()
            elif char == '-':
                self.tokens.append(Token(TokenType.MINUS, '-', self.line, col))
                self.advance()
            elif char == '*':
                self.tokens.append(Token(TokenType.MULTIPLY, '*', self.line, col))
                self.advance()
            elif char == '/':
                self.tokens.append(Token(TokenType.DIVIDE, '/', self.line, col))
                self.advance()
            elif char == '^':
                self.tokens.append(Token(TokenType.POWER, '^', self.line, col))
                self.advance()
            elif char == '(':
                self.tokens.append(Token(TokenType.LPAREN, '(', self.line, col))
                self.advance()
            elif char == ')':
                self.tokens.append(Token(TokenType.RPAREN, ')', self.line, col))
                self.advance()
            elif char == ',':
                self.tokens.append(Token(TokenType.COMMA, ',', self.line, col))
                self.advance()
            else:
                self.error(f"Unexpected character: {char}")
                self.advance()
        
        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return self.tokens
