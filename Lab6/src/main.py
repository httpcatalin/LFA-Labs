from ast_nodes import BinaryOpNode, FunctionCallNode, IdentifierNode, NumberNode, UnaryOpNode
from lexer import Lexer
from parser import Parser, ParserError
from tokens import TokenType


def render_ast(node, indent: int = 0) -> str:
    spacing = "  " * indent

    if isinstance(node, NumberNode):
        return f"{spacing}Number({node.value})"

    if isinstance(node, IdentifierNode):
        return f"{spacing}Identifier({node.name})"

    if isinstance(node, UnaryOpNode):
        lines = [f"{spacing}UnaryOp({node.operator})"]
        lines.append(render_ast(node.operand, indent + 1))
        return "\n".join(lines)

    if isinstance(node, BinaryOpNode):
        lines = [f"{spacing}BinaryOp({node.operator})"]
        lines.append(render_ast(node.left, indent + 1))
        lines.append(render_ast(node.right, indent + 1))
        return "\n".join(lines)

    if isinstance(node, FunctionCallNode):
        lines = [f"{spacing}FunctionCall({node.name})"]
        if not node.arguments:
            lines.append(f"{'  ' * (indent + 1)}(no arguments)")
        else:
            for argument in node.arguments:
                lines.append(render_ast(argument, indent + 1))
        return "\n".join(lines)

    return f"{spacing}UnknownNode"


def print_tokens(tokens):
    for token in tokens:
        if token.type == TokenType.EOF:
            print(f"  {token}")
            continue
        print(f"  {token}")


def run_case(description: str, expression: str):
    print("\n" + "=" * 88)
    print(f"Case: {description}")
    print(f"Input: {expression}")

    lexer = Lexer(expression)
    tokens = lexer.tokenize()

    print("Tokens:")
    print_tokens(tokens)

    parser = Parser(tokens)
    try:
        ast = parser.parse()
        print("AST:")
        print(render_ast(ast))
    except ParserError as error:
        print(f"Parser error: {error}")


def main():
    print("=" * 88)
    print("LAB 6 - PARSER AND ABSTRACT SYNTAX TREE")
    print("=" * 88)

    test_cases = [
        ("Simple precedence", "2 + 3 * 4"),
        ("Nested functions", "sin(x) + cos(y)"),
        ("Unary operator and division", "-sqrt(16) + tan(y) / 2"),
        ("Right-associative power", "2 ^ 3 ^ 2"),
        ("Multiple function arguments", "sin(x, y + 1)"),
        ("Grouped expression", "((2 + 3) * sin(0.5))"),
        ("Lexical error", "x @ y"),
        ("Syntax error", "sin(2 + )"),
    ]

    for description, expression in test_cases:
        run_case(description, expression)

    print("\n" + "=" * 88)
    print("DONE")
    print("=" * 88)


if __name__ == "__main__":
    main()
