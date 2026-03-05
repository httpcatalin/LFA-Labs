from finite_automaton import FiniteAutomaton


def build_original_fa():
    states = {"S", "A", "B", "FINAL"}
    alphabet = {"a", "b", "c"}
    start = "S"
    finals = {"FINAL"}

    transitions = {
        "S": {"a": {"S"}, "b": {"S"}, "c": {"A"}},
        "A": {"a": {"B"}},
        "B": {"a": {"B"}, "b": {"B"}, "c": {"FINAL"}},
    }

    return FiniteAutomaton(states, alphabet, transitions, start, finals)


def build_modified_ndfa():
    states = {"S", "A", "B", "FINAL"}
    alphabet = {"a", "b", "c"}
    start = "S"
    finals = {"FINAL"}

    transitions = {
        "S": {"a": {"S", "A"}, "b": {"S"}, "c": {"A"}},
        "A": {"a": {"B"}},
        "B": {"a": {"B"}, "b": {"B"}, "c": {"FINAL"}},
    }

    return FiniteAutomaton(states, alphabet, transitions, start, finals)


def main():
    print("\na) FA to Regular Grammar")
    fa = build_original_fa()
    grammar = fa.to_regular_grammar()
    grammar.pretty_print()

    print("\nb) Determinism check")
    fa.print_table("Original FA")
    print(f"\n  Is deterministic: {fa.is_deterministic()}")

    print("\nc) NDFA -> DFA conversion")
    ndfa = build_modified_ndfa()
    ndfa.print_table("NDFA (modified)")
    print(f"  Is deterministic: {ndfa.is_deterministic()}")

    dfa = ndfa.ndfa_to_dfa()
    dfa.print_table("DFA after subset construction")
    print(f"  Is deterministic: {dfa.is_deterministic()}")

    print("\nd) Graphical representation")
    fa.draw(filename="fa_original.png", title="Original FA")
    dfa.draw(filename="fa_dfa.png", title="DFA after conversion")


if __name__ == "__main__":
    main()