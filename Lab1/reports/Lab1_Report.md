# Grammar to Finite Automaton Conversion - Variant 15

### Course: Formal Languages & Finite Automata

### Author: Catalin Bitca

---

## Theory

A formal grammar is defined as a 4-tuple \( G = (V_N, V_T, P, S) \), where:

- \(V_N\) is the set of non-terminals,
- \(V_T\) is the set of terminals,
- \(P\) is the set of production rules,
- \(S\) is the start symbol.

For this laboratory work, the implemented grammar is right-linear and has:

- **VN** = {S, D, E, F, L}
- **VT** = {a, b, c, d}

**Productions**:

- S -> aD
- D -> bE
- E -> cF | dL
- F -> dD
- L -> aL | bL | c

Because the grammar is right-linear, it can be converted into a finite automaton.
In this lab, the idea was not only to write code that works, but to understand why each production can be seen as a transition and how this theory is used in practice.

---

## Objectives

- Implement a `Grammar` class for word generation and conversion to finite automaton.
- Implement a `FiniteAutomaton` class for language membership checking.
- Demonstrate generated words and validation results in `main.py`.
- Better understand the connection between regular grammars and automata by implementing both sides.

---

## Laboratory Work Description

In this laboratory, I started from the grammar definition and then tried to represent it as clearly as possible in Python.
At first, the implementation looked simple on paper, but when I connected all components (`Grammar`, conversion method, automaton simulation, and tests), I realized that small details matter a lot.

The implementation is split into three files:

- `grammar.py` - definition of the `Grammar` class.
- `finite_automaton.py` - definition of the `FiniteAutomaton` class.
- `main.py` - grammar construction, generation, and testing.

### Grammar class

The `Grammar` class stores `vn`, `vt`, `productions`, and `start_symbol`.

The `generate_string()` method creates valid words deterministically using an internal counter (`self._counter`) and pattern composition:

- fixed prefix `ab`,
- optional repeated block `cdb`,
- mandatory `d`,
- optional tail of `a`,
- final `c`.

The `to_finite_automaton()` method converts productions into transitions. For terminal-only productions (like `L -> c`), it adds a transition to a synthetic final state `Qf`.

From my perspective as a student, this conversion step was the most important part of the lab because it forced me to think in terms of states and transitions, not just strings.

### FiniteAutomaton class

The automaton stores transitions as sets of target states (`dict[state][symbol] -> set(states)`), so matching is done with a set of current states. The method `string_belong_to_language()`:

- starts from `{start_state}`,
- updates the frontier for each input symbol,
- rejects if no state is reachable,
- accepts if any reachable state is final after consuming all symbols.

I chose this approach because it is flexible and works naturally if a state can have multiple transitions for the same symbol.

## Difficulties Encountered

During this laboratory, the hardest part was making sure that the grammar and automaton behaviors were perfectly aligned.

What I found difficult:

- Making sure each production rule is translated correctly to a transition.
- Handling final productions (like `L -> c`) in code by introducing a dedicated final state (`Qf`).
- Keeping the report synchronized with the actual code and output, because even small code changes can make old explanations wrong.

What helped me solve these issues:

- Printing multiple generated words and validating them immediately.
- Testing both positive and negative examples.
- Re-reading the grammar-to-automaton correspondence rule by rule.

---

## Code Snippets

### `Grammar.generate_string()`

```python
def generate_string(self):
    k = self._counter
    self._counter += 1
    loop_count = k % 3
    tail_len = k % 4
    parts = ["a", "b"]
    for _ in range(loop_count):
        parts.extend(["c", "d", "b"])
    parts.append("d")
    parts.extend(["a"] * tail_len)
    parts.append("c")
    return "".join(parts)
```

### `Grammar.to_finite_automaton()`

```python
def to_finite_automaton(self):
    from finite_automaton import FiniteAutomaton

    states = set(self.vn)
    final_state = "Qf"
    states.add(final_state)
    alphabet = set(self.vt)
    transitions = {}
    for left, rights in self.productions.items():
        for right in rights:
            if len(right) == 1:
                symbol = right[0]
                transitions.setdefault(left, {}).setdefault(symbol, set()).add(final_state)
            else:
                symbol = right[0]
                next_state = right[1]
                transitions.setdefault(left, {}).setdefault(symbol, set()).add(next_state)
    return FiniteAutomaton(states, alphabet, transitions, self.start_symbol, {final_state})
```

### `FiniteAutomaton.string_belong_to_language()`

```python
def string_belong_to_language(self, input_string):
    current_states = {self.start_state}
    for symbol in input_string:
        next_states = set()
        for state in current_states:
            state_transitions = self.transitions.get(state, {})
            for target in state_transitions.get(symbol, set()):
                next_states.add(target)
        current_states = next_states
        if not current_states:
            return False
    return any(state in self.final_states for state in current_states)
```

---

## Results

From the language structure induced by the grammar, accepted words follow:

```text
ab(cdb)*d(a|b)*c
```

Program output (`python3 -u Lab1/src/main.py`):

```text
word 1: abdc
word 2: abcdbdac
word 3: abcdbcdbdaac
word 4: abdaaac
word 5: abcdbdc
abdc -> True
abcdbdac -> True
abcdbcdbdaac -> True
abdaaac -> True
abcdbdc -> True
abdc -> True
abccc -> False
ac -> False
abd -> False
```

The output confirms that generated words are accepted, while invalid samples (`abccc`, `ac`, `abd`) are rejected.

Overall, this laboratory helped me understand much better how formal language theory becomes executable logic. Implementing both classes made the topic clearer than only studying it theoretically.
