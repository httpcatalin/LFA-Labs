from dataclasses import dataclass
from enum import Enum, auto


class TokenType(Enum):
    INTEGER = auto()
    FLOAT = auto()
    IDENTIFIER = auto()
    FUNCTION = auto()

    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    POWER = auto()

    LPAREN = auto()
    RPAREN = auto()
    COMMA = auto()

    EOF = auto()
    ERROR = auto()


@dataclass(frozen=True)
class Token:
    type: TokenType
    value: object
    line: int
    column: int

    def __repr__(self) -> str:
        return f"Token({self.type.name}, {repr(self.value)}, {self.line}, {self.column})"
