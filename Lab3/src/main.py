from lexer import Lexer

def print_tokens(description, code):
    print(f"\n{'='*60}")
    print(f"Input: {description}")
    print(f"Code: {code}")
    print(f"{'='*60}")
    
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    print(f"Tokens:")
    for token in tokens:
        if token.type.name != 'EOF':
            print(f"  {token}")
    print(f"  {tokens[-1]}")

def main():
    print("\n" + "="*60)
    print("LEXICAL ANALYZER - Mathematical Expression Language")
    print("="*60)
    
    test_cases = [
        ("Simple addition", "2 + 3"),
        ("Float multiplication", "3.14 * 2.5"),
        ("Sine function", "sin(0.5)"),
        ("Cosine with variable", "cos(x)"),
        ("Complex expression", "sin(x) + cos(y) * 2.5"),
        ("Power operator", "2 ^ 8"),
        ("Square root", "sqrt(16)"),
        ("Multiple arguments", "sin(x) - tan(y) / 2"),
        ("Nested parentheses", "((2 + 3) * sin(0.5))"),
        ("Expression with comment", "x + 5  # this is a comment"),
        ("Variable names", "var1 + var_2 + x3"),
        ("Invalid character", "x @ y"),
        ("E-notation attempt", "2.5e-3"),
    ]
    
    for description, code in test_cases:
        print_tokens(description, code)
    
    print("\n" + "="*60)
    print("LEXICAL ANALYSIS COMPLETE")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
