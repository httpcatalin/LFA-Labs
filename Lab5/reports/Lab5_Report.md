# Lab 5: Chomsky Normal Form Conversion (Variant 7)

### Course: Formal Languages & Finite Automata

### Author: Catalin Bitca

---

## Theory

A context-free grammar is defined as $G = (V_N, V_T, P, S)$, where:

- $V_N$ is the set of non-terminals,
- $V_T$ is the set of terminals,
- $P$ is the set of productions,
- $S$ is the start symbol.

A grammar is in **Chomsky Normal Form (CNF)** if every production has one of the following forms:

- $A \to BC$, where $A, B, C \in V_N$,
- $A \to a$, where $A \in V_N$ and $a \in V_T$,
- optionally $S \to \varepsilon$ if the language contains the empty word.

To transform a CFG into CNF, a standard normalization pipeline is used:

1. eliminate $\varepsilon$-productions,
2. eliminate unit productions (renamings),
3. eliminate inaccessible symbols,
4. eliminate non-productive symbols,
5. convert remaining productions to CNF-compatible binary or terminal form.

---

## Objectives

1. Understand Chomsky Normal Form and why it is useful.
2. Implement all required grammar normalization stages.
3. Execute and test the conversion for Variant 7.
4. Keep execution simple: run Variant 7 directly without command-line arguments.

---

## Variant 7

Original variant statement:

```text
1. Eliminate ε productions.
2. Eliminate any renaming.
3. Eliminate inaccessible symbols.
4. Eliminate the non productive symbols.
5. Obtain the Chomsky Normal Form.
```

Given grammar (as provided in the variant):

```text
G = (V_N, V_T, P, S)
V_N = {S, A, B, C, E}
V_T = {a, b}

P = {
    1.  S -> bA
    2.  S -> B
    3.  A -> a
    4.  A -> aS
    5.  A -> bAaAb
    6.  B -> AC
    7.  B -> bS
    8.  B -> aAa
    9.  C -> AB
    10. C -> AB
    11. E -> BA
}
```

Equivalent grouped form used in code:

```text
G = (V_N, V_T, P, S)
V_N = {S, A, B, C, E}
V_T = {a, b}

S -> bA | B
A -> a | aS | bAaAb
B -> AC | bS | aAa
C -> AB
E -> BA
```

The implementation accepts duplicate productions as well; internally, productions are stored as sets, so duplicates are automatically removed.

---

## Implementation Description

Files used:

- `Lab5/src/grammar.py`
- `Lab5/src/main.py`

### 1. Grammar Representation

The grammar is represented by the `ContextFreeGrammar` dataclass:

- `vn`: set of non-terminals,
- `vt`: set of terminals,
- `productions`: dictionary `left -> set of RHS tuples`,
- `start_symbol`: start non-terminal.

Using tuples and sets makes transformations deterministic and removes duplicate rules naturally.

### 2. Normalization Pipeline

The pipeline is implemented as separate methods:

- `eliminate_epsilon_productions()`
- `eliminate_unit_productions()`
- `eliminate_inaccessible_symbols()`
- `eliminate_non_productive_symbols()`
- `to_cnf()`

Each stage returns a new grammar object, so intermediate grammars can be printed and verified.

### 3. CNF Conversion Details

During CNF conversion:

- terminals that appear in long productions are replaced with dedicated aliases (for example `T_A_1 -> a`, `T_B_1 -> b`),
- productions longer than 2 symbols are binarized by introducing helper non-terminals (`X1`, `X2`, ...).

This guarantees final productions satisfy CNF constraints.

### 4. Execution Style

For this task, the implementation runs directly on Variant 7 and does not require command-line arguments.

Run command:

```bash
python main.py
```

---

## Code Snippets

### Epsilon Elimination

```python
def eliminate_epsilon_productions(self) -> "ContextFreeGrammar":
    nullable = self._nullable_nonterminals()
    new_productions = {left: set() for left in self.vn}

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
```

### Unit Production Elimination

```python
def eliminate_unit_productions(self) -> "ContextFreeGrammar":
    unit_closure = {left: {left} for left in self.vn}

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

    new_productions = {left: set() for left in self.vn}

    for left in self.vn:
        for target in unit_closure[left]:
            for rhs in self.productions.get(target, set()):
                if len(rhs) == 1 and rhs[0] in self.vn:
                    continue
                new_productions[left].add(rhs)

    return ContextFreeGrammar(set(self.vn), set(self.vt), new_productions, self.start_symbol)
```

### CNF Conversion Entry

```python
def to_cnf(self) -> "ContextFreeGrammar":
    vn = set(self.vn)
    productions = {
        left: set(rights)
        for left, rights in self.productions.items()
    }

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

    # replace terminals in long productions and binarize RHS with length > 2
    # ...

    return ContextFreeGrammar(vn, set(self.vt), cnf_productions, self.start_symbol)
```

---

## Execution and Results

Command used:

```bash
cd Lab5/src
python main.py
```

Observed stages:

1. **Eliminate $\varepsilon$-productions**: no change (none present).
2. **Eliminate unit productions**: `S -> B` removed; productions of `B` were propagated into `S`.
3. **Eliminate inaccessible symbols**: `E` removed (not reachable from `S`).
4. **Eliminate non-productive symbols**: no extra removals.
5. **Convert to CNF**: helper non-terminals introduced for terminals in long rules and for binarization.

Final CNF grammar obtained:

```text
A -> a | T_A_1 S | T_B_1 X1
B -> AC | T_A_1 X4 | T_B_1 S
C -> AB
S -> AC | T_A_1 X5 | T_B_1 A | T_B_1 S
T_A_1 -> a
T_B_1 -> b
X1 -> A X2
X2 -> T_A_1 X3
X3 -> A T_B_1
X4 -> A T_A_1
X5 -> A T_A_1
```

Program validation output:

```text
Grammar is CNF: True
```

---

## Difficulties Encountered

1. Correctly handling nullable combinations during epsilon elimination without introducing invalid empty rules.
2. Preserving deterministic and readable output across all transformation stages.
3. Converting long mixed productions like `bAaAb` into valid binary CNF form while keeping the transformation readable.

---

## Conclusion

The laboratory requirements were implemented end-to-end: all normalization stages were executed in the specified order, intermediate grammars were displayed, and the final grammar was validated as CNF. The final Lab 5 script now runs directly on Variant 7 with no command-line arguments, which keeps execution straightforward for evaluation.

## References

- Course materials: Formal Languages & Finite Automata, TUM
- Chomsky Normal Form overview: https://en.wikipedia.org/wiki/Chomsky_normal_form
