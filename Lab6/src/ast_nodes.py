from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class NumberNode:
    value: int | float


@dataclass(frozen=True)
class IdentifierNode:
    name: str


@dataclass(frozen=True)
class UnaryOpNode:
    operator: str
    operand: "ASTNode"


@dataclass(frozen=True)
class BinaryOpNode:
    left: "ASTNode"
    operator: str
    right: "ASTNode"


@dataclass(frozen=True)
class FunctionCallNode:
    name: str
    arguments: tuple["ASTNode", ...]


ASTNode = NumberNode | IdentifierNode | UnaryOpNode | BinaryOpNode | FunctionCallNode
