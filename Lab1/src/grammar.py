class Grammar:
    def __init__(self, vn, vt, productions, start_symbol):
        self.vn = vn
        self.vt = vt
        self.productions = productions
        self.start_symbol = start_symbol
        self._counter = 0

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
        start_state = self.start_symbol
        final_states = {final_state}
        return FiniteAutomaton(states, alphabet, transitions, start_state, final_states)
