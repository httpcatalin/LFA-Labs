from finite_automaton import FiniteAutomaton
from grammar import Grammar

def build_fa_variant7():
    states = {"q0", "q1", "q2", "q3"}
    alphabet = {"a", "b"}
    transitions = {
        "q0": {"a": {"q1"}},
        "q1": {"b": {"q2"}, "a": {"q1"}},
        "q2": {"b": {"q3", "q2"}},
        "q3": {"a": {"q1"}}
    }
    start_state = "q0"
    final_states = {"q3"}
    return FiniteAutomaton(states, alphabet, transitions, start_state, final_states)

def main():
    fa = build_fa_variant7()
    print("Is deterministic:", fa.is_deterministic())
    rg = fa.to_regular_grammar()
    print("Grammar type:", rg.classify_chomsky())
    dfa = fa.ndfa_to_dfa()
    print("DFA states:", dfa.states)
    print("DFA transitions:", dfa.transitions)
    print("DFA final states:", dfa.final_states)
    try:
        dot = fa.to_graphviz()
        dot.render('fa_variant7', format='png', cleanup=True)
        print("Graph saved as fa_variant7.png")
    except ImportError:
        print("Graphviz not installed, skipping graphical representation")

if __name__ == "__main__":
    main()