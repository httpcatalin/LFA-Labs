class FiniteAutomaton:
    def __init__(self, states, alphabet, transitions, start_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.final_states = final_states

    def string_belong_to_language(self, input_string):
        current = {self.start_state}
        for symbol in input_string:
            next_states = set()
            for state in current:
                next_states.update(self.transitions.get(state, {}).get(symbol, set()))
            current = next_states
            if not current:
                return False
        return bool(current & self.final_states)

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
            prods = []
            for symbol in sorted(self.alphabet):
                targets = self.transitions.get(state, {}).get(symbol, set())
                for target in sorted(targets):
                    prods.append([symbol, target])
                    if target in self.final_states:
                        prods.append([symbol])
            productions[state] = prods
        return Grammar(vn, vt, productions, self.start_state)

    def ndfa_to_dfa(self):
        from collections import deque

        def state_name(state_set):
            return "{" + ",".join(sorted(state_set)) + "}"

        start = frozenset([self.start_state])
        queue = deque([start])
        visited = {start}
        dfa_transitions = {}
        dfa_final = set()

        while queue:
            current = queue.popleft()
            name = state_name(current)
            dfa_transitions[name] = {}
            for symbol in sorted(self.alphabet):
                next_set = set()
                for s in current:
                    next_set.update(self.transitions.get(s, {}).get(symbol, set()))
                if next_set:
                    nf = frozenset(next_set)
                    nn = state_name(nf)
                    dfa_transitions[name][symbol] = {nn}
                    if nf not in visited:
                        visited.add(nf)
                        queue.append(nf)
            if current & self.final_states:
                dfa_final.add(name)

        dfa_states = {state_name(s) for s in visited}
        return FiniteAutomaton(dfa_states, self.alphabet, dfa_transitions,
                               state_name(start), dfa_final)

    def draw_graph(self, filename, title="Finite Automaton"):
        import graphviz
        dot = graphviz.Digraph(format="png")
        dot.attr(rankdir="LR", label=title, fontsize="16")
        dot.node("", shape="none", width="0", height="0")
        dot.edge("", self.start_state)

        for state in sorted(self.states):
            if state in self.final_states and state == self.start_state:
                dot.node(state, shape="doublecircle", style="filled", fillcolor="lightyellow")
            elif state in self.final_states:
                dot.node(state, shape="doublecircle", style="filled", fillcolor="lightgreen")
            elif state == self.start_state:
                dot.node(state, shape="circle", style="filled", fillcolor="lightblue")
            else:
                dot.node(state, shape="circle")

        edges = {}
        for state in sorted(self.states):
            for symbol in sorted(self.alphabet):
                targets = self.transitions.get(state, {}).get(symbol, set())
                for target in sorted(targets):
                    edges.setdefault((state, target), []).append(symbol)

        for (src, dst), symbols in sorted(edges.items()):
            dot.edge(src, dst, label=",".join(symbols))

        dot.render(filename, cleanup=True)