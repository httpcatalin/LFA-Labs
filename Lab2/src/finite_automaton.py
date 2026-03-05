class FiniteAutomaton:
    def __init__(self, states, alphabet, transitions, start_state, final_states):
        self.states = set(states)
        self.alphabet = set(alphabet)
        self.start_state = start_state
        self.final_states = set(final_states)
        self.transitions = self._normalize_transitions(transitions)

    @staticmethod
    def _normalize_transitions(transitions):
        normalized = {}
        for state, sym_map in transitions.items():
            normalized[state] = {}
            for symbol, targets in sym_map.items():
                normalized[state][symbol] = set(targets)
        return normalized

    @staticmethod
    def _set_name(state_set):
        return "{" + ",".join(sorted(state_set)) + "}"

    def to_regular_grammar(self):
        from grammar import Grammar

        productions = {}
        for state, sym_map in self.transitions.items():
            productions[state] = []
            for symbol, targets in sym_map.items():
                for target in sorted(targets):
                    if target in self.final_states:
                        productions[state].append(symbol)
                    else:
                        productions[state].append(f"{symbol}{target}")
        return Grammar(productions)

    def is_deterministic(self):
        for sym_map in self.transitions.values():
            for targets in sym_map.values():
                if len(targets) > 1:
                    return False
        return True

    def ndfa_to_dfa(self):
        start_set = frozenset([self.start_state])
        unmarked = [start_set]
        visited = {start_set}
        dfa_transitions = {}
        dfa_finals = set()

        while unmarked:
            current = unmarked.pop()
            current_name = self._set_name(current)
            dfa_transitions[current_name] = {}

            for symbol in sorted(self.alphabet):
                next_set = set()
                for state in current:
                    next_set.update(self.transitions.get(state, {}).get(symbol, set()))

                if not next_set:
                    continue

                next_frozen = frozenset(next_set)
                next_name = self._set_name(next_frozen)
                dfa_transitions[current_name][symbol] = {next_name}

                if next_frozen not in visited:
                    visited.add(next_frozen)
                    unmarked.append(next_frozen)

            if current & self.final_states:
                dfa_finals.add(current_name)

        dfa_states = set(dfa_transitions.keys())
        for sym_map in dfa_transitions.values():
            for targets in sym_map.values():
                dfa_states.update(targets)

        return FiniteAutomaton(
            states=dfa_states,
            alphabet=self.alphabet,
            transitions=dfa_transitions,
            start_state=self._set_name(start_set),
            final_states=dfa_finals,
        )

    def print_table(self, title):
        print(f"\n{title}")
        symbols = sorted(self.alphabet)
        print(f"{'State':<20}" + "".join(f"{s:<20}" for s in symbols))

        for state in sorted(self.states):
            prefix = ("*" if state in self.final_states else "") + ("->" if state == self.start_state else "")
            row = f"{prefix + state:<20}"
            for sym in symbols:
                targets = sorted(self.transitions.get(state, {}).get(sym, set()))
                row += f"{str(targets if targets else '-'):<20}"
            print(row)

    def draw(self, filename="fa.png", title="Finite Automaton"):
        try:
            import matplotlib.pyplot as plt
            import matplotlib.patches as mpatches
            import networkx as nx
        except ImportError:
            print("matplotlib/networkx not installed, skipping graphical representation")
            return

        graph = nx.MultiDiGraph()
        for state in self.states:
            graph.add_node(state)

        edge_labels = {}
        for state, sym_map in self.transitions.items():
            for symbol, targets in sym_map.items():
                for target in targets:
                    graph.add_edge(state, target)
                    key = (state, target)
                    edge_labels[key] = edge_labels.get(key, "") + symbol + ","

        edge_labels = {key: value.rstrip(",") for key, value in edge_labels.items()}

        positions = nx.spring_layout(graph, seed=42, k=2)
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.set_title(title, fontsize=13)
        ax.axis("off")

        node_colors = []
        for node in graph.nodes():
            if node in self.final_states:
                node_colors.append("#90ee90")
            elif node == self.start_state:
                node_colors.append("#add8e6")
            else:
                node_colors.append("#ffffff")

        nx.draw_networkx_nodes(
            graph,
            positions,
            node_size=1800,
            node_color=node_colors,
            edgecolors="black",
            linewidths=1.5,
            ax=ax,
        )
        nx.draw_networkx_labels(graph, positions, font_size=11, ax=ax)
        nx.draw_networkx_edges(
            graph,
            positions,
            ax=ax,
            arrows=True,
            arrowstyle="-|>",
            arrowsize=20,
            connectionstyle="arc3,rad=0.15",
            edge_color="gray",
            width=1.5,
        )

        for (u, v), label in edge_labels.items():
            x = (positions[u][0] + positions[v][0]) / 2
            y = (positions[u][1] + positions[v][1]) / 2 + 0.1
            ax.text(
                x,
                y,
                label,
                fontsize=9,
                ha="center",
                bbox=dict(boxstyle="round,pad=0.2", fc="lightyellow", ec="gray"),
            )

        legend = [
            mpatches.Patch(color="#add8e6", label="Start state"),
            mpatches.Patch(color="#90ee90", label="Final state"),
            mpatches.Patch(color="white", label="Normal state", linewidth=1),
        ]
        ax.legend(handles=legend, loc="upper left", fontsize=9)

        plt.tight_layout()
        plt.savefig(filename, dpi=150)
        plt.close()
        print(f"Graph saved to {filename}")