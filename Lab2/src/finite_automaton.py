class FiniteAutomaton:
    def __init__(self, states, alphabet, transitions, start_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.final_states = final_states

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

    def is_deterministic(self):
        for state in self.states:
            for symbol in self.alphabet:
                targets = self.transitions.get(state, {}).get(symbol, set())
                if len(targets) > 1:
                    return False
        return True

    def to_regular_grammar(self):
        from grammar import Grammar
        vn = set(self.states)
        vt = set(self.alphabet)
        productions = {}
        for state in self.states:
            productions[state] = []
            for symbol, targets in self.transitions.get(state, {}).items():
                for target in targets:
                    if target in self.final_states:
                        productions[state].append([symbol])
                    else:
                        productions[state].append([symbol, target])
            if state in self.final_states:
                productions[state].append([])
        return Grammar(vn, vt, productions, self.start_state)

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

    def to_graphviz(self):
        import graphviz
        dot = graphviz.Digraph()
        for state in self.states:
            if state in self.final_states:
                dot.node(state, shape='doublecircle')
            else:
                dot.node(state)
        dot.node(self.start_state, color='green')
        for state, trans in self.transitions.items():
            for symbol, targets in trans.items():
                for target in targets:
                    dot.edge(state, target, label=symbol)
        return dot