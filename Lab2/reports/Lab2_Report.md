# Lab 2 Report: Determinism in Finite Automata. Conversion from NDFA to DFA. Chomsky Hierarchy.

### Course: Formal Languages & Finite Automata

### Author: Cătălin Bîtca

### Date: 26 February 2026

---

## Theory

Finite automata can be deterministic or non-deterministic. A DFA has exactly one transition per state and symbol, while an NDFA can have multiple or none. The Chomsky hierarchy classifies grammars: Type 3 regular, Type 2 context-free, Type 1 context-sensitive, Type 0 unrestricted. Conversion from FA to regular grammar maps states to non-terminals and transitions to productions.

## Objectives

- Add grammar classification based on Chomsky hierarchy.
- Implement FA to regular grammar conversion.
- Determine if FA is deterministic.
- Implement NDFA to DFA conversion.
- Optionally, graphical representation of FA.

## Implementation description

- Grammar class includes classify_chomsky method to check production rules for hierarchy type.
- FiniteAutomaton class has is_deterministic to check for single transitions, to_regular_grammar to convert to grammar, ndfa_to_dfa using subset construction, and to_graphviz for visualization.
- Main file defines variant 7 FA, checks determinism, converts to grammar and DFA, and generates graph.

Code snippets:

```python
def classify_chomsky(self):
    is_regular = True
    is_context_free = True
    is_context_sensitive = True
    for left, rights in self.productions.items():
        if len(left) != 1 or left not in self.vn:
            is_context_free = False
            is_regular = False
        for right in rights:
            if len(right) == 0:
                continue
            if len(right) == 1:
                if right[0] not in self.vt:
                    is_regular = False
            elif len(right) == 2:
                if not (right[0] in self.vt and right[1] in self.vn):
                    is_regular = False
            else:
                is_regular = False
            if len(left) > len(right):
                is_context_sensitive = False
    if is_regular:
        return 3
    elif is_context_free:
        return 2
    elif is_context_sensitive:
        return 1
    else:
        return 0
```

```python
def ndfa_to_dfa(self):
    from collections import deque
    dfa_states = []
    dfa_transitions = {}
    dfa_final_states = set()
    queue = deque()
    start_set = frozenset([self.start_state])
    dfa_states.append(start_set)
    queue.append(start_set)
    state_map = {start_set: 'q0'}
    state_counter = 1
    while queue:
        current_set = queue.popleft()
        current_name = state_map[current_set]
        dfa_transitions[current_name] = {}
        for symbol in self.alphabet:
            next_set = set()
            for state in current_set:
                targets = self.transitions.get(state, {}).get(symbol, set())
                next_set.update(targets)
            if next_set:
                next_frozenset = frozenset(next_set)
                if next_frozenset not in state_map:
                    state_map[next_frozenset] = f'q{state_counter}'
                    state_counter += 1
                    dfa_states.append(next_frozenset)
                    queue.append(next_frozenset)
                dfa_transitions[current_name][symbol] = state_map[next_frozenset]
        if any(state in self.final_states for state in current_set):
            dfa_final_states.add(current_name)
    dfa_alphabet = self.alphabet
    dfa_start_state = 'q0'
    return FiniteAutomaton(set(state_map.values()), dfa_alphabet, dfa_transitions, dfa_start_state, dfa_final_states)
```

## Results

For variant 7 FA: non-deterministic due to multiple transitions from q2 on b. Converted to regular grammar of type 3. NDFA to DFA creates states for subsets. Graph saved if graphviz available.

## Conclusions

Implemented all required functionalities. FA is NDFA, converted to DFA and grammar. Graphical representation optional.

## References

- Course notes and lab instructions.
