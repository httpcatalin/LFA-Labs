import argparse

from grammar import ContextFreeGrammar, build_variant_7_grammar, json_input_template


def print_header(title: str):
    print("\n" + "=" * 90)
    print(title)
    print("=" * 90)


def print_stage(index: int, title: str, grammar: ContextFreeGrammar):
    print_header(f"STEP {index}: {title}")
    print(grammar.to_pretty_string())
    print(f"Production count: {grammar.production_count()}")


def load_input_grammar(args) -> tuple[ContextFreeGrammar, str]:
    if args.grammar_file:
        grammar = ContextFreeGrammar.from_json_file(args.grammar_file)
        return grammar, "Custom grammar loaded from JSON"

    grammar = build_variant_7_grammar()
    return grammar, "Variant 7 grammar"


def main():
    parser = argparse.ArgumentParser(
        description="Normalize a context-free grammar to Chomsky Normal Form"
    )
    parser.add_argument(
        "--grammar-file",
        type=str,
        help="Path to JSON grammar file",
    )
    parser.add_argument(
        "--show-json-template",
        action="store_true",
        help="Print JSON template for custom grammar input",
    )
    args = parser.parse_args()

    if args.show_json_template:
        print(json_input_template())
        return

    grammar, label = load_input_grammar(args)

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
