from grammar import Grammar


def build_grammar():
    vn = {"S", "D", "E", "F", "L"}
    vt = {"a", "b", "c", "d"}
    productions = {
        "S": [["a", "D"]],
        "D": [["b", "E"]],
        "E": [["c", "F"], ["d", "L"]],
        "F": [["d", "D"]],
        "L": [["a", "L"], ["b", "L"], ["c"]],
    }
    return Grammar(vn, vt, productions, "S")


def main():
    grammar = build_grammar()
    words = [grammar.generate_string() for _ in range(5)]
    for i, word in enumerate(words, start=1):
        print(f"word {i}: {word}")

    fa = grammar.to_finite_automaton()
    tests = words + ["abdc", "abccc", "ac", "abd"]
    for word in tests:
        result = fa.string_belong_to_language(word)
        print(f"{word} -> {result}")


if __name__ == "__main__":
    main()
