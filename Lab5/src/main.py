from grammar import ContextFreeGrammar, build_variant_7_grammar


def print_header(title: str):
    print("\n" + "=" * 90)
    print(title)
    print("=" * 90)


def print_stage(index: int, title: str, grammar: ContextFreeGrammar):
    print_header(f"STEP {index}: {title}")
    print(grammar.to_pretty_string())
    print(f"Production count: {grammar.production_count()}")


def main():
    grammar = build_variant_7_grammar()
    label = "Variant 7 grammar"

    print_header("LAB 5 - CHOMSKY NORMAL FORM")
    print(label)

    step_0 = grammar
    step_1 = step_0.eliminate_epsilon_productions()
    step_2 = step_1.eliminate_unit_productions()
    step_3 = step_2.eliminate_inaccessible_symbols()
    step_4 = step_3.eliminate_non_productive_symbols()
    step_5 = step_4.to_cnf()

    print_stage(0, "Original grammar", step_0)
    print_stage(1, "Eliminate epsilon productions", step_1)
    print_stage(2, "Eliminate unit productions (renaming)", step_2)
    print_stage(3, "Eliminate inaccessible symbols", step_3)
    print_stage(4, "Eliminate non-productive symbols", step_4)
    print_stage(5, "Convert to Chomsky Normal Form", step_5)

    print_header("CNF VALIDATION")
    print(f"Grammar is CNF: {step_5.is_cnf()}")


if __name__ == "__main__":
    main()
