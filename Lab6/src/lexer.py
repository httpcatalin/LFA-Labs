import re

from tokens import Token, TokenType


class Lexer:
    TOKEN_SPECS = [
        ("WHITESPACE", r"\s+"),
        ("COMMENT", r"#[^\n]*"),
        ("FLOAT", r"\d+\.\d+"),
        ("INTEGER", r"\d+"),
        ("FUNCTION", r"\b(?:sin|cos|tan|sqrt)\b"),
        ("IDENTIFIER", r"[A-Za-z_][A-Za-z0-9_]*"),
        ("PLUS", r"\+"),
        ("MINUS", r"-"),
        ("MULTIPLY", r"\*"),
        ("DIVIDE", r"/"),
        ("POWER", r"\^"),
        ("LPAREN", r"\("),
        ("RPAREN", r"\)"),
        ("COMMA", r","),
        ("MISMATCH", r"."),
    ]

    MASTER_PATTERN = re.compile(
        "|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPECS),
        re.MULTILINE,
    )

    def __init__(self, text: str):
        self.text = text

    def tokenize(self) -> list[Token]:
        tokens: list[Token] = []
        position = 0
        line = 1
        line_start = 0

        while position < len(self.text):
            match = self.MASTER_PATTERN.match(self.text, position)
            if match is None:
                column = position - line_start + 1
                tokens.append(Token(TokenType.ERROR, f"Unexpected character: {self.text[position]}", line, column))
                position += 1
                continue

            token_kind = match.lastgroup
            lexeme = match.group(token_kind)
            column = position - line_start + 1
            end_position = match.end()

            if token_kind not in {"WHITESPACE", "COMMENT"}:
                if token_kind == "MISMATCH":
                    tokens.append(Token(TokenType.ERROR, f"Unexpected character: {lexeme}", line, column))
                else:
                    token_type = TokenType[token_kind]
                    token_value = self._convert_value(token_kind, lexeme)
                    tokens.append(Token(token_type, token_value, line, column))

            line_break_count = lexeme.count("\n")
            if line_break_count:
                line += line_break_count
                last_newline_index = lexeme.rfind("\n")
                line_start = end_position - (len(lexeme) - last_newline_index - 1)

            position = end_position

        eof_column = position - line_start + 1
        tokens.append(Token(TokenType.EOF, None, line, eof_column))
        return tokens

    @staticmethod
    def _convert_value(token_kind: str, lexeme: str):
        if token_kind == "INTEGER":
            return int(lexeme)
        if token_kind == "FLOAT":
            return float(lexeme)
        return lexeme
