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
