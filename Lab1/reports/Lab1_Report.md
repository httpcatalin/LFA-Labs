# Lab 1 Report: Formal Grammar and Finite Automaton

### Course: Formal Languages & Finite Automata

### Author: Cătălin Bîtca

### Date: 11 February 2026

---

## Theory

A formal language is defined by an alphabet, a vocabulary made of words from that alphabet, and a set of grammar rules that describe how valid words are formed. A grammar provides the production rules, while a finite automaton is an equivalent computational model that checks if a word belongs to the language. For a right-linear grammar, the conversion to a finite automaton is direct by mapping productions to transitions.

## Objectives

- Understand the components of a formal language and a grammar.
- Implement a grammar based on the given variant.
- Generate valid strings from the grammar.
- Convert the grammar to a finite automaton.
- Verify strings using the finite automaton.

## Implementation description

- Grammar is represented by sets $V_N$, $V_T$, a production dictionary, and a start symbol. It can generate valid strings using a simple deterministic pattern that follows the grammar.
- Finite automaton stores states, alphabet, transitions, start state, and final states; it checks membership by simulating transitions over the input string.
- A main file builds the grammar, generates five words, converts to a finite automaton, and tests several strings.

Code snippets:

```python
class Grammar:
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

```python
class FiniteAutomaton:
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

## Results

Running the program prints five valid words and then shows whether each test string is accepted by the finite automaton. The generated words are accepted, while invalid strings are rejected.

## Conclusions

The grammar and finite automaton models represent the same language. The conversion from right-linear grammar to a finite automaton is straightforward, and the automaton correctly verifies membership.

## References

- Course notes and lab instructions.
