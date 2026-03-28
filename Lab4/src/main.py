import argparse

from regex_engine import RegexGenerator


DEFAULT_VARIANT_3_REGEXES = [
    "O(P|Q|R)+2(3|4)",
    "A*B(C|D|E)F(G|H|I)^2",
    "J+K(L|M|N)*O?(P|Q)^3",
]

EXPECTED_VARIANT_3_EXAMPLES = {
    "O(P|Q|R)+2(3|4)": ["OPP23", "OQQQQ24"],
    "A*B(C|D|E)F(G|H|I)^2": ["AAABCFGG", "AAAAABDFHH"],
    "J+K(L|M|N)*O?(P|Q)^3": ["JJKLOPPP", "JKNQQQ"],
}


def format_set_preview(words):
    if not words:
        return "{}"
    preview = ", ".join(words)
    return "{" + preview + "}"


def pick_evenly(words, limit):
    if limit is None or limit >= len(words):
        return words
    if limit <= 0:
        return []

    if limit == 1:
        return [words[0]]

    selected = []
    last_index = len(words) - 1
    for i in range(limit):
        index = round(i * last_index / (limit - 1))
        selected.append(words[index])
    return list(dict.fromkeys(selected))


def print_processing_steps(steps):
    print("Processing sequence:")
    for step in steps:
        print(f"  {step}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate valid words for regular expressions using dynamic parsing"
    )
    parser.add_argument(
        "--regex",
        action="append",
        dest="regexes",
        help="Regex to process (can be used multiple times)",
    )
    parser.add_argument(
        "--max-repeat",
        type=int,
        default=5,
        help="Upper limit for unbounded repetitions (* and +)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=30,
        help="Maximum number of words shown per regex",
    )
    parser.add_argument(
        "--show-steps",
        action="store_true",
        help="Show sequence of regex processing steps",
    )
    args = parser.parse_args()

    regexes = args.regexes if args.regexes else DEFAULT_VARIANT_3_REGEXES
    generator = RegexGenerator(max_unbounded_repetitions=args.max_repeat)

    print("=" * 80)
    print("LAB 4 - REGULAR EXPRESSIONS (VARIANT 3)")
    print("=" * 80)
    print(f"Unbounded repetition limit: {args.max_repeat}")
    print(f"Output limit per regex: {args.limit}")

    for index, regex in enumerate(regexes, start=1):
        print("\n" + "-" * 80)
        print(f"Regex {index}: {regex}")
        try:
            words, steps = generator.generate(regex, limit=None)
            shown_words = pick_evenly(words, args.limit)
            print(f"Generated words count (total): {len(words)}")
            print(f"Generated words count (shown): {len(shown_words)}")
            print(format_set_preview(shown_words))

            expected_words = EXPECTED_VARIANT_3_EXAMPLES.get(regex, [])
            if expected_words:
                all_present = all(word in words for word in expected_words)
                status = "yes" if all_present else "no"
                print(f"Required examples generated: {status}")
                if not all_present:
                    missing = [word for word in expected_words if word not in words]
                    print(f"Missing examples: {', '.join(missing)}")
            if args.show_steps:
                print_processing_steps(steps)
        except ValueError as error:
            print(f"Error while processing regex: {error}")

    print("\n" + "=" * 80)
    print("DONE")
    print("=" * 80)


if __name__ == "__main__":
    main()
