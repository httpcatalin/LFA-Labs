from enum import Enum, auto

class TokenType(Enum):
    INTEGER = auto()
    FLOAT = auto()
    IDENTIFIER = auto()
    
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    POWER = auto()
    
    LPAREN = auto()
    RPAREN = auto()
    COMMA = auto()
    
    SIN = auto()
    COS = auto()
    TAN = auto()
    SQRT = auto()
    
    EOF = auto()
    ERROR = auto()

class Token:
    def __init__(self, type_, value, line, column):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column
    
    def __repr__(self):
        return f"Token({self.type.name}, {repr(self.value)}, {self.line}, {self.column})"
