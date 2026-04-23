from ast_nodes import BinaryOpNode, FunctionCallNode, IdentifierNode, NumberNode, UnaryOpNode
from tokens import Token, TokenType


class ParserError(Exception):
    pass


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.position = 0

    def parse(self):
        lexical_errors = [token for token in self.tokens if token.type == TokenType.ERROR]
        if lexical_errors:
            first_error = lexical_errors[0]
            raise ParserError(
                f"Lexical error at line {first_error.line}, column {first_error.column}: {first_error.value}"
            )

        node = self._parse_expression()
        self._consume(TokenType.EOF, "Expected end of input")
        return node

    def _parse_expression(self):
        node = self._parse_term()

        while self._current().type in {TokenType.PLUS, TokenType.MINUS}:
            operator = self._advance()
            right = self._parse_term()
            node = BinaryOpNode(node, operator.value, right)

        return node

    def _parse_term(self):
        node = self._parse_power()

        while self._current().type in {TokenType.MULTIPLY, TokenType.DIVIDE}:
            operator = self._advance()
            right = self._parse_power()
            node = BinaryOpNode(node, operator.value, right)

        return node

    def _parse_power(self):
        node = self._parse_unary()

        if self._current().type == TokenType.POWER:
            operator = self._advance()
            right = self._parse_power()
            node = BinaryOpNode(node, operator.value, right)

        return node

    def _parse_unary(self):
        if self._current().type in {TokenType.PLUS, TokenType.MINUS}:
            operator = self._advance()
            operand = self._parse_unary()
            return UnaryOpNode(operator.value, operand)

        return self._parse_primary()

    def _parse_primary(self):
        token = self._current()

        if token.type in {TokenType.INTEGER, TokenType.FLOAT}:
            self._advance()
            return NumberNode(token.value)

        if token.type in {TokenType.IDENTIFIER, TokenType.FUNCTION}:
            if self._peek().type == TokenType.LPAREN:
                return self._parse_function_call()
            self._advance()
            return IdentifierNode(str(token.value))

        if token.type == TokenType.LPAREN:
            self._advance()
            expression = self._parse_expression()
            self._consume(TokenType.RPAREN, "Expected ')' after expression")
            return expression

        self._error(f"Unexpected token '{token.value}'")

    def _parse_function_call(self):
        function_name = str(self._current().value)
        self._advance()
        self._consume(TokenType.LPAREN, "Expected '(' after function name")

        arguments = []
        if self._current().type != TokenType.RPAREN:
            arguments.append(self._parse_expression())
            while self._current().type == TokenType.COMMA:
                self._advance()
                arguments.append(self._parse_expression())

        self._consume(TokenType.RPAREN, "Expected ')' after function arguments")
        return FunctionCallNode(function_name, tuple(arguments))

    def _consume(self, expected_type: TokenType, message: str):
        token = self._current()
        if token.type != expected_type:
            self._error(message)
        return self._advance()

    def _advance(self):
        current = self._current()
        if self.position < len(self.tokens) - 1:
            self.position += 1
        return current

    def _current(self):
        return self.tokens[self.position]

    def _peek(self, offset: int = 1):
        index = min(self.position + offset, len(self.tokens) - 1)
        return self.tokens[index]

    def _error(self, message: str):
        token = self._current()
        raise ParserError(f"{message} at line {token.line}, column {token.column}")
