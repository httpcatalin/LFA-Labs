class Grammar:
    def __init__(self, vn, vt, productions, start_symbol):
        self.vn = vn
        self.vt = vt
        self.productions = productions
        self.start_symbol = start_symbol

    def classify_chomsky(self):
        is_right_linear = True

        for left, rights in self.productions.items():
            if left not in self.vn:
                return "Type 0 (Unrestricted)"

            for right in rights:
                if len(right) == 0:
                    continue
                elif len(right) == 1:
                    if right[0] not in self.vt:
                        is_right_linear = False
                elif len(right) == 2:
                    if not (right[0] in self.vt and right[1] in self.vn):
                        is_right_linear = False
                else:
                    is_right_linear = False

        if is_right_linear:
            return "Type 3 (Regular)"
        return "Type 2 (Context-Free)"