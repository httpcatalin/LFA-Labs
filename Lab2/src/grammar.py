class Grammar:
    def __init__(self, productions):
        self.productions = productions

    def pretty_print(self):
        for state in sorted(self.productions.keys()):
            right_side = self.productions[state]
            if right_side:
                print(f"  {state} -> {' | '.join(right_side)}")