from finite_automaton import FiniteAutomaton
from grammar import Grammar


def main():
    lab1_grammar = Grammar(
        vn={"S", "D", "E", "F", "L"},
        vt={"a", "b", "c", "d"},
        productions={
            "S": [["a", "D"]],
            "D": [["b", "E"]],
            "E": [["c", "F"], ["d", "L"]],
            "F": [["d", "D"]],
            "L": [["a", "L"], ["b", "L"], ["c"]],
        },
        start_symbol="S"
    )
    print(f"Lab 1 Grammar classification: {lab1_grammar.classify_chomsky()}")

    print("\n--- Task 3: Variant 7 Finite Automaton ---")
    fa = FiniteAutomaton(
        states={"q0", "q1", "q2", "q3"},
        alphabet={"a", "b"},
        transitions={
            "q0": {"a": {"q1"}},
            "q1": {"b": {"q2"}, "a": {"q1"}},
            "q2": {"b": {"q2", "q3"}},
            "q3": {"a": {"q1"}}
        },
        start_state="q0",
        final_states={"q3"}
    )

    print("\n--- 3a: FA to Regular Grammar ---")
    grammar = fa.to_regular_grammar()
    print(f"Non-terminals (Vn): {sorted(grammar.vn)}")
    print(f"Terminals (Vt): {sorted(grammar.vt)}")
    print(f"Start symbol: {grammar.start_symbol}")
    print("Productions:")
    for left in sorted(grammar.productions):
        for right in grammar.productions[left]:
            print(f"  {left} -> {''.join(right) if right else 'epsilon'}")
    print(f"Grammar classification: {grammar.classify_chomsky()}")

    print("\n--- 3b: Determinism Check ---")
    print(f"The FA is deterministic: {fa.is_deterministic()}")

    print("\n--- 3c: NDFA to DFA Conversion ---")
    dfa = fa.ndfa_to_dfa()
    print(f"DFA states: {sorted(dfa.states)}")
    print(f"DFA start state: {dfa.start_state}")
    print(f"DFA final states: {sorted(dfa.final_states)}")
    print("DFA transitions:")
    for state in sorted(dfa.transitions):
        for symbol in sorted(dfa.transitions[state]):
            targets = dfa.transitions[state][symbol]
            for t in sorted(targets):
                print(f"  d({state}, {symbol}) = {t}")
    print(f"DFA is deterministic: {dfa.is_deterministic()}")

    print("\n--- String Testing (NFA vs DFA) ---")
    test_strings = ["abb", "abbb", "aabb", "abbabb", "ab", "a", "b", "abba", "abbabbb"]
    for s in test_strings:
        nfa_res = fa.string_belong_to_language(s)
        dfa_res = dfa.string_belong_to_language(s)
        print(f"  '{s}': NFA={nfa_res}, DFA={dfa_res}")

    print("\n--- 3d: Graphical Representation ---")
    import os
    images_dir = os.path.join(os.path.dirname(__file__), "..", "images")
    os.makedirs(images_dir, exist_ok=True)
    try:
        fa.draw_graph(os.path.join(images_dir, "nfa_variant7"), title="NFA - Variant 7")
        print("NFA graph saved to Lab2/images/nfa_variant7.png")
        dfa.draw_graph(os.path.join(images_dir, "dfa_variant7"), title="DFA - Variant 7 (after conversion)")
        print("DFA graph saved to Lab2/images/dfa_variant7.png")
    except Exception as e:
        print(f"Could not generate graphs: {e}")


if __name__ == "__main__":
    main()