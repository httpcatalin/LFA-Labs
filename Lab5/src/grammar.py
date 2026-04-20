import json
from dataclasses import dataclass
from itertools import combinations


EPSILON_SYMBOLS = {"", "ε", "epsilon", "eps", "lambda", "λ"}


@dataclass
class ContextFreeGrammar:
    vn: set[str]
    vt: set[str]
    productions: dict[str, set[tuple[str, ...]]]
    start_symbol: str

    @classmethod
    def from_raw(
        cls,
        vn: set[str],
        vt: set[str],
        productions: dict[str, list[str] | list[list[str]] | list[tuple[str, ...]]],
        start_symbol: str,
    ) -> "ContextFreeGrammar":
        symbols = set(vn) | set(vt)
        normalized_productions: dict[str, set[tuple[str, ...]]] = {}

        for left in vn:
            normalized_productions[left] = set()

        for left, rights in productions.items():
            if left not in vn:
                continue
            for right in rights:
                rhs = cls._normalize_rhs(right, symbols)
                normalized_productions[left].add(rhs)

        return cls(set(vn), set(vt), normalized_productions, start_symbol)

    @classmethod
    def from_json_file(cls, file_path: str) -> "ContextFreeGrammar":
        with open(file_path, "r", encoding="utf-8") as handle:
            data = json.load(handle)

        vn = set(data["vn"])
        vt = set(data["vt"])
        start_symbol = data["start_symbol"]
        productions = data["productions"]
        return cls.from_raw(vn, vt, productions, start_symbol)

    @staticmethod
    def _normalize_rhs(raw_rhs, symbols: set[str]) -> tuple[str, ...]:
        if raw_rhs is None:
            return ()

        if isinstance(raw_rhs, str):
            rhs_text = raw_rhs.strip()
            if rhs_text in EPSILON_SYMBOLS:
                return ()
            if " " in rhs_text:
                parts = [part for part in rhs_text.split(" ") if part]
                return tuple(parts)
            return tuple(ContextFreeGrammar._tokenize_compact(rhs_text, symbols))

        if isinstance(raw_rhs, (list, tuple)):
            if len(raw_rhs) == 0:
                return ()
            if len(raw_rhs) == 1 and str(raw_rhs[0]).strip() in EPSILON_SYMBOLS:
                return ()
            return tuple(str(symbol) for symbol in raw_rhs)

        raise TypeError(f"Unsupported RHS type: {type(raw_rhs)}")

    @staticmethod
    def _tokenize_compact(rhs_text: str, symbols: set[str]) -> list[str]:
        if not rhs_text:
            return []

        ordered_symbols = sorted(symbols, key=lambda symbol: (-len(symbol), symbol))
        tokens: list[str] = []
        index = 0

        while index < len(rhs_text):
            matched = False
            for symbol in ordered_symbols:
                if rhs_text.startswith(symbol, index):
                    tokens.append(symbol)
                    index += len(symbol)
                    matched = True
                    break
            if not matched:
                tokens.append(rhs_text[index])
                index += 1

        return tokens

    def copy(self) -> "ContextFreeGrammar":
        copied_productions = {
            left: set(rights)
            for left, rights in self.productions.items()
        }
        return ContextFreeGrammar(set(self.vn), set(self.vt), copied_productions, self.start_symbol)

    def eliminate_epsilon_productions(self) -> "ContextFreeGrammar":
        nullable = self._nullable_nonterminals()
        new_productions: dict[str, set[tuple[str, ...]]] = {left: set() for left in self.vn}

        for left in self.vn:
            for rhs in self.productions.get(left, set()):
                if len(rhs) == 0:
                    continue

                nullable_positions = [
                    index
                    for index, symbol in enumerate(rhs)
                    if symbol in nullable
                ]

                for count in range(len(nullable_positions) + 1):
                    for selected in combinations(nullable_positions, count):
                        selected_indexes = set(selected)
                        candidate = tuple(
                            symbol
                            for index, symbol in enumerate(rhs)
                            if index not in selected_indexes
                        )
                        if len(candidate) > 0:
                            new_productions[left].add(candidate)
                        elif left == self.start_symbol and self.start_symbol in nullable:
                            new_productions[left].add(())

        if self.start_symbol in nullable:
            new_productions[self.start_symbol].add(())

        return ContextFreeGrammar(set(self.vn), set(self.vt), new_productions, self.start_symbol)

    def _nullable_nonterminals(self) -> set[str]:
        nullable: set[str] = set()
        changed = True

        while changed:
            changed = False
            for left in self.vn:
                if left in nullable:
                    continue
                for rhs in self.productions.get(left, set()):
                    if len(rhs) == 0:
                        nullable.add(left)
                        changed = True
                        break
                    if all(symbol in nullable for symbol in rhs):
                        nullable.add(left)
                        changed = True
                        break

        return nullable

    def eliminate_unit_productions(self) -> "ContextFreeGrammar":
        unit_closure: dict[str, set[str]] = {left: {left} for left in self.vn}

        for source in self.vn:
            stack = [source]
            while stack:
                current = stack.pop()
                for rhs in self.productions.get(current, set()):
                    if len(rhs) == 1 and rhs[0] in self.vn:
                        target = rhs[0]
                        if target not in unit_closure[source]:
                            unit_closure[source].add(target)
                            stack.append(target)

        new_productions: dict[str, set[tuple[str, ...]]] = {left: set() for left in self.vn}

        for left in self.vn:
            for target in unit_closure[left]:
                for rhs in self.productions.get(target, set()):
                    if len(rhs) == 1 and rhs[0] in self.vn:
                        continue
                    new_productions[left].add(rhs)

        return ContextFreeGrammar(set(self.vn), set(self.vt), new_productions, self.start_symbol)

    def eliminate_inaccessible_symbols(self) -> "ContextFreeGrammar":
        reachable: set[str] = {self.start_symbol}
        stack = [self.start_symbol]

        while stack:
            current = stack.pop()
            for rhs in self.productions.get(current, set()):
                for symbol in rhs:
                    if symbol in self.vn and symbol not in reachable:
                        reachable.add(symbol)
                        stack.append(symbol)

        new_productions: dict[str, set[tuple[str, ...]]] = {left: set() for left in reachable}

        for left in reachable:
            for rhs in self.productions.get(left, set()):
                if all(symbol not in self.vn or symbol in reachable for symbol in rhs):
                    new_productions[left].add(rhs)

        return ContextFreeGrammar(reachable, set(self.vt), new_productions, self.start_symbol)

    def eliminate_non_productive_symbols(self) -> "ContextFreeGrammar":
        productive: set[str] = set()
        changed = True

        while changed:
            changed = False
            for left in self.vn:
                if left in productive:
                    continue
                for rhs in self.productions.get(left, set()):
                    if all(symbol in self.vt or symbol in productive for symbol in rhs):
                        productive.add(left)
                        changed = True
                        break

        if self.start_symbol not in productive:
            return ContextFreeGrammar(
                {self.start_symbol},
                set(self.vt),
                {self.start_symbol: set()},
                self.start_symbol,
            )

        kept_non_terminals = {left for left in self.vn if left in productive}
        new_productions: dict[str, set[tuple[str, ...]]] = {left: set() for left in kept_non_terminals}

        for left in kept_non_terminals:
            for rhs in self.productions.get(left, set()):
                if all(symbol in self.vt or symbol in kept_non_terminals for symbol in rhs):
                    new_productions[left].add(rhs)

        used_terminals = {
            symbol
            for rights in new_productions.values()
            for rhs in rights
            for symbol in rhs
            if symbol in self.vt
        }
        if not used_terminals:
            used_terminals = set(self.vt)

        return ContextFreeGrammar(kept_non_terminals, used_terminals, new_productions, self.start_symbol)

    def to_cnf(self) -> "ContextFreeGrammar":
        vn = set(self.vn)
        productions: dict[str, set[tuple[str, ...]]] = {
            left: set(rights)
            for left, rights in self.productions.items()
        }

        for left in vn:
            productions.setdefault(left, set())

        terminal_aliases: dict[str, str] = {}

        def new_non_terminal(prefix: str) -> str:
            index = 1
            while True:
                candidate = f"{prefix}{index}"
                if candidate not in vn and candidate not in self.vt:
                    vn.add(candidate)
                    productions.setdefault(candidate, set())
                    return candidate
                index += 1

        replaced_productions: dict[str, set[tuple[str, ...]]] = {left: set() for left in vn}

        for left in sorted(vn):
            for rhs in productions.get(left, set()):
                if len(rhs) >= 2:
                    replaced_rhs = []
                    for symbol in rhs:
                        if symbol in self.vt:
                            if symbol not in terminal_aliases:
                                alias = new_non_terminal(f"T_{symbol.upper()}_")
                                terminal_aliases[symbol] = alias
                            replaced_rhs.append(terminal_aliases[symbol])
                        else:
                            replaced_rhs.append(symbol)
                    replaced_productions[left].add(tuple(replaced_rhs))
                else:
                    replaced_productions[left].add(rhs)

        for terminal, alias in terminal_aliases.items():
            replaced_productions.setdefault(alias, set()).add((terminal,))

        cnf_productions: dict[str, set[tuple[str, ...]]] = {
            left: set() for left in vn
        }

        for left in sorted(replaced_productions):
            for rhs in replaced_productions[left]:
                if len(rhs) <= 2:
                    cnf_productions[left].add(rhs)
                    continue

                current_left = left
                symbols = list(rhs)
                while len(symbols) > 2:
                    first = symbols.pop(0)
                    middle = new_non_terminal("X")
                    cnf_productions.setdefault(current_left, set()).add((first, middle))
                    current_left = middle
                cnf_productions.setdefault(current_left, set()).add(tuple(symbols))

        for left in vn:
            cnf_productions.setdefault(left, set())

        return ContextFreeGrammar(vn, set(self.vt), cnf_productions, self.start_symbol)

    def is_cnf(self) -> bool:
        for left in self.vn:
            for rhs in self.productions.get(left, set()):
                if len(rhs) == 0:
                    if left != self.start_symbol:
                        return False
                elif len(rhs) == 1:
                    if rhs[0] not in self.vt:
                        return False
                elif len(rhs) == 2:
                    if rhs[0] not in self.vn or rhs[1] not in self.vn:
                        return False
                else:
                    return False
        return True

    def production_count(self) -> int:
        return sum(len(rights) for rights in self.productions.values())

    def to_pretty_string(self) -> str:
        lines = []
        lines.append(f"Vn = {{{', '.join(sorted(self.vn))}}}")
        lines.append(f"Vt = {{{', '.join(sorted(self.vt))}}}")
        lines.append(f"Start = {self.start_symbol}")
        lines.append("Productions:")

        for left in sorted(self.vn):
            rights = self.productions.get(left, set())
            if not rights:
                continue
            formatted_rights = [
                self._format_rhs(rhs)
                for rhs in sorted(rights, key=self._rhs_sort_key)
            ]
            lines.append(f"  {left} -> {' | '.join(formatted_rights)}")

        if all(not self.productions.get(left, set()) for left in self.vn):
            lines.append("  (no productions)")

        return "\n".join(lines)

    @staticmethod
    def _rhs_sort_key(rhs: tuple[str, ...]) -> tuple[int, str]:
        return len(rhs), ContextFreeGrammar._format_rhs(rhs)

    @staticmethod
    def _format_rhs(rhs: tuple[str, ...]) -> str:
        if len(rhs) == 0:
            return "ε"
        if all(len(symbol) == 1 for symbol in rhs):
            return "".join(rhs)
        return " ".join(rhs)


def build_variant_7_grammar() -> ContextFreeGrammar:
    vn = {"S", "A", "B", "C", "E"}
    vt = {"a", "b"}
    productions = {
        "S": ["bA", "B"],
        "A": ["a", "aS", "bAaAb"],
        "B": ["AC", "bS", "aAa"],
        "C": ["AB"],
        "E": ["BA"],
    }
    return ContextFreeGrammar.from_raw(vn, vt, productions, "S")


def json_input_template() -> str:
    template = {
        "vn": ["S", "A", "B"],
        "vt": ["a", "b"],
        "start_symbol": "S",
        "productions": {
            "S": ["aA", "B"],
            "A": ["a", "aS", "epsilon"],
            "B": ["b", "AB"],
        },
    }
    return json.dumps(template, indent=2)
