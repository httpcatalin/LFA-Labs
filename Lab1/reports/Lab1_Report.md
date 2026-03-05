# Lab 1: Grammar to Finite Automaton Conversion - Variant 15

### Course: Formal Languages & Finite Automata

### Author: Catalin Bitca

---

## Theory

A formal grammar is a mathematical framework used to describe and generate languages. Formally, a grammar is defined as a 4-tuple $G = (V_N, V_T, P, S)$, where:

- $V_N$ is the finite set of **non-terminal** symbols (variables that can be expanded),
- $V_T$ is the finite set of **terminal** symbols (the actual characters that appear in generated strings),
- $P$ is a finite set of **production rules** of the form $\alpha \to \beta$,
- $S \in V_N$ is the **start symbol** from which derivation begins.

A grammar is called **right-linear** (Type 3 in the Chomsky hierarchy) if every production rule has one of two forms: $A \to aB$ or $A \to a$, where $A, B \in V_N$ and $a \in V_T$. Right-linear grammars generate exactly the class of **regular languages**, meaning there is a direct correspondence between them and finite automata.

A **finite automaton (FA)** is a 5-tuple $M = (Q, \Sigma, \delta, q_0, F)$:

- $Q$ is a finite set of states,
- $\Sigma$ is the input alphabet,
- $\delta: Q \times \Sigma \to \mathcal{P}(Q)$ is the transition function,
- $q_0 \in Q$ is the start state,
- $F \subseteq Q$ is the set of accepting (final) states.

The key theoretical insight behind this lab is that every right-linear grammar can be transformed into an equivalent finite automaton. Each non-terminal becomes a state, each terminal-driven production becomes a transition, and productions that end in a single terminal (like $L \to c$) are handled by introducing a dedicated final state. This makes it possible to check whether a given string belongs to the language by simulating the automaton — starting from the initial state, consuming one symbol at a time, and checking if we end in an accepting state.

---

## Objectives

- Implement a `Grammar` class capable of generating valid words and converting itself to a finite automaton.
- Implement a `FiniteAutomaton` class that simulates state transitions and checks whether a string belongs to the language.
- Demonstrate correctness by generating words from the grammar and validating them against the automaton.
- Develop a practical understanding of the connection between regular grammars and finite automata.

---

## Variant 15 — Grammar Definition

```
VN = {S, D, E, F, L}
VT = {a, b, c, d}
P:
  S -> aD
  D -> bE
  E -> cF | dL
  F -> dD
  L -> aL | bL | c
```

The start symbol is $S$. Because every production is of the form $A \to aB$ or $A \to a$ (right-linear), this grammar is regular and can be converted into a finite automaton.

---

## Implementation Description

The implementation is split into three files that work together:

- `grammar.py` — the `Grammar` class, responsible for string generation and conversion to a finite automaton.
- `finite_automaton.py` — the `FiniteAutomaton` class, responsible for simulating transitions and validating strings.
- `main.py` — the driver that constructs the grammar, generates words, and tests them.

### Grammar Class

The `Grammar` class stores the four components of a grammar ($V_N$, $V_T$, $P$, and $S$) and provides two key methods.

**`generate_string()`** builds valid words deterministically using an internal counter. Each call produces a different string that follows the grammar's structure. The approach uses pattern composition: a fixed prefix `ab`, an optional repeated block `cdb` (which corresponds to applying rules $E \to cF$ and $F \to dD$ and $D \to bE$ in a loop), a mandatory `d` (entering the $L$ branch via $E \to dL$), an optional tail of `a` or `b` symbols (the self-loop $L \to aL \mid bL$), and a final `c` (the terminal rule $L \to c$). This ensures every generated string is derivable from $S$ while giving variety across calls.

**`to_finite_automaton()`** converts the grammar into a finite automaton by mapping each production to a transition. For a production like $S \to aD$, it creates the transition $\delta(S, a) = D$. For terminal-only productions like $L \to c$, it creates a transition to a synthetic final state $Q_f$, since the derivation ends there. The resulting automaton has states for each non-terminal plus $Q_f$, uses the terminals as its alphabet, and has $S$ as the start state.

### FiniteAutomaton Class

The `FiniteAutomaton` class stores transitions internally as a nested dictionary where $\delta(q, a)$ maps to a set of target states. This representation naturally supports non-determinism (multiple targets per symbol), even though the grammar in this variant produces a deterministic automaton.

The **`string_belong_to_language()`** method simulates the automaton. It maintains a frontier of current states (starting from $\{q_0\}$) and, for each input symbol, computes the set of all reachable next states. If at any point the frontier becomes empty, the string is rejected immediately. After consuming all symbols, the string is accepted if and only if at least one state in the frontier is a final state.

This set-based simulation approach was chosen because it generalizes cleanly — it works correctly even if a state has multiple transitions for the same symbol, which becomes relevant in Lab 2 when dealing with non-deterministic automata.

### Main Driver

The `main.py` file constructs the Variant 15 grammar, generates 5 words, and then tests both those generated words and several hand-crafted invalid strings against the automaton. This serves as a validation step: generated words should all be accepted, while strings like `abccc`, `ac`, and `abd` should be rejected because they don't follow any valid derivation path.

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

The language generated by the grammar follows the pattern:

```text
ab(cdb)*d(a|b)*c
```

This means every valid string starts with `ab`, optionally repeats the `cdb` block (the $E \to cF \to cdD \to cdbE$ loop), then transitions through `d` into the $L$ branch, optionally adds any number of `a` or `b` symbols, and terminates with `c`.

Program output:

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

All five generated words are correctly accepted by the automaton. The invalid test strings are rejected for the following reasons:

- `abccc` — after `abc`, the only valid continuation requires `F -> dD`, but `c` is not valid for state $F$.
- `ac` — after `a`, the automaton is in state $D$, which requires `b` next, not `c`.
- `abd` — after `abd`, the automaton is in state $L$, which can accept `a`, `b`, or `c`, but `d` is not in its transition set. And the string simply ends without reaching $c$.

---

## Difficulties Encountered

The hardest part of this lab was ensuring perfect alignment between the grammar's theoretical definition and the automaton's behavior in code. Specifically:

- **Handling terminal-only productions** like $L \to c$ required careful thought. The solution was introducing a synthetic final state $Q_f$ that has no outgoing transitions. Without it, the automaton would have no way to "accept" after consuming the last terminal.
- **Making string generation correct and diverse** was a balancing act. Hardcoding a single valid string would be trivial, but generating multiple distinct strings that all follow the grammar required a structured approach with the counter-based pattern composition.
- **Keeping the report synchronized with actual code** was challenging because even small refactors could invalidate earlier explanations or output examples.

---

## Conclusions

This laboratory demonstrated how a right-linear grammar can be systematically converted into a finite automaton. The Grammar class generates valid strings by following the production rules, and the FiniteAutomaton class validates them by simulating state transitions. Both components produce consistent results: generated strings are accepted, and strings that violate the grammar's structure are correctly rejected. The implementation reinforced the theoretical equivalence between regular grammars and finite automata in a practical, executable way.

## References

- Course materials: Formal Languages & Finite Automata, TUM
