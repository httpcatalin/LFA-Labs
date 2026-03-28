from dataclasses import dataclass
from itertools import product


@dataclass(frozen=True)
class Literal:
    value: str


@dataclass(frozen=True)
class Concat:
    parts: tuple


@dataclass(frozen=True)
class UnionNode:
    options: tuple


@dataclass(frozen=True)
class Repeat:
    node: object
    min_times: int
    max_times: int | None


class RegexParser:
    def __init__(self, pattern: str):
        self.pattern = pattern.replace(" ", "")
        self.pos = 0
        self.steps = []

    def parse(self):
        self._step(f"Start parsing: {self.pattern}")
        node = self._parse_expression()
        if self._current() is not None:
            raise ValueError(f"Unexpected symbol '{self._current()}' at position {self.pos}")
        self._step("Parsing finished")
        return node

    def _parse_expression(self):
        terms = [self._parse_term()]
        while self._current() == "|":
            self._consume("|")
            self._step("Apply union operator '|' ")
            terms.append(self._parse_term())
        if len(terms) == 1:
            return terms[0]
        return UnionNode(tuple(terms))

    def _parse_term(self):
        factors = []
        while True:
            current = self._current()
            if current is None or current in ")|":
                break
            factors.append(self._parse_factor())
        if not factors:
            return Literal("")
        if len(factors) == 1:
            return factors[0]
        self._step("Build concatenation")
        return Concat(tuple(factors))

    def _parse_factor(self):
        atom = self._parse_atom()
        while True:
            current = self._current()
            if current == "*":
                self._consume("*")
                self._step("Apply '*' (0..infinity)")
                atom = Repeat(atom, 0, None)
            elif current == "+":
                self._consume("+")
                self._step("Apply '+' (1..infinity)")
                atom = Repeat(atom, 1, None)
            elif current == "?":
                self._consume("?")
                self._step("Apply '?' (0..1)")
                atom = Repeat(atom, 0, 1)
            elif current == "^":
                self._consume("^")
                number = self._parse_number()
                self._step(f"Apply exponent '^{number}'")
                atom = Repeat(atom, number, number)
            else:
                break
        return atom

    def _parse_atom(self):
        current = self._current()
        if current is None:
            raise ValueError("Unexpected end of regex")
        if current == "(":
            self._consume("(")
            self._step("Enter group '('")
            node = self._parse_expression()
            if self._current() != ")":
                raise ValueError(f"Missing ')' at position {self.pos}")
            self._consume(")")
            self._step("Exit group ')' ")
            return node
        if current in "|)*+?^":
            raise ValueError(f"Unexpected symbol '{current}' at position {self.pos}")
        literal = self._consume()
        self._step(f"Read literal '{literal}'")
        return Literal(literal)

    def _parse_number(self):
        if self._current() is None or not self._current().isdigit():
            raise ValueError(f"Expected number after '^' at position {self.pos}")
        start = self.pos
        while self._current() is not None and self._current().isdigit():
            self.pos += 1
        return int(self.pattern[start:self.pos])

    def _consume(self, expected=None):
        current = self._current()
        if current is None:
            raise ValueError("Unexpected end of regex")
        if expected is not None and current != expected:
            raise ValueError(f"Expected '{expected}', got '{current}'")
        self.pos += 1
        return current

    def _current(self):
        if self.pos >= len(self.pattern):
            return None
        return self.pattern[self.pos]

    def _step(self, message: str):
        self.steps.append(f"{len(self.steps) + 1}. {message}")


class RegexGenerator:
    def __init__(self, max_unbounded_repetitions=5):
        self.max_unbounded_repetitions = max_unbounded_repetitions

    def build(self, regex: str):
        parser = RegexParser(regex)
        ast = parser.parse()
        return ast, parser.steps

    def generate(self, regex: str, limit=None):
        ast, steps = self.build(regex)
        words = self._expand(ast)
        words = list(dict.fromkeys(words))
        if limit is not None:
            words = words[:limit]
        return words, steps

    def _expand(self, node):
        if isinstance(node, Literal):
            return [node.value]

        if isinstance(node, UnionNode):
            result = []
            for option in node.options:
                result.extend(self._expand(option))
            return result

        if isinstance(node, Concat):
            expanded_parts = [self._expand(part) for part in node.parts]
            result = []
            for combo in product(*expanded_parts):
                result.append("".join(combo))
            return result

        if isinstance(node, Repeat):
            max_times = node.max_times
            if max_times is None:
                max_times = self.max_unbounded_repetitions
            result = []
            subwords = self._expand(node.node)
            for count in range(node.min_times, max_times + 1):
                if count == 0:
                    result.append("")
                    continue
                pools = [subwords] * count
                for combo in product(*pools):
                    result.append("".join(combo))
            return result

        raise TypeError(f"Unknown AST node type: {type(node)}")
