# Lab 6: Parser and Abstract Syntax Tree

### Course: Formal Languages & Finite Automata

### Author: Catalin Bitca

---

## Theory

**Parsing** is the stage that follows lexical analysis. While the lexer transforms a character stream into tokens, the parser verifies whether the token sequence follows the grammar of the language and builds a structural representation of the input.

A common representation produced during syntactic analysis is the **parse tree**. A related and more compact representation is the **Abstract Syntax Tree (AST)**. The AST preserves the essential syntactic structure of an expression while omitting unnecessary grammatical details.

In this laboratory, parsing is applied to the mathematical-expression language from Lab 3. The parser is implemented as a recursive-descent parser with operator precedence and associativity, and it constructs AST nodes for numbers, identifiers, unary operators, binary operators, and function calls.

---

## Objectives

1. Understand parsing and syntactic analysis.
2. Understand the AST concept and its role in compiler pipelines.
3. Extend the Lab 3 language with:
   - explicit `TokenType` categorization,
   - regular-expression based token type recognition,
   - AST data structures,
   - a simple parser that extracts syntactic information.

---

## Language Specification

The input language supports:

- Numeric literals: integers and floating-point numbers.
- Identifiers: variable names such as `x`, `var1`, `result_value`.
- Function names: `sin`, `cos`, `tan`, `sqrt`.
- Operators: `+`, `-`, `*`, `/`, `^`.
- Grouping and argument separators: `(`, `)`, `,`.

Token categories are represented by `TokenType`:

- `INTEGER`, `FLOAT`, `IDENTIFIER`, `FUNCTION`
- `PLUS`, `MINUS`, `MULTIPLY`, `DIVIDE`, `POWER`
- `LPAREN`, `RPAREN`, `COMMA`
- `EOF`, `ERROR`

All token categories are identified in the lexer using regular expressions.

---

## Grammar Used by the Parser

A precedence-aware grammar was implemented:

```text
expression  -> term ( ("+" | "-") term )*
term        -> power ( ("*" | "/") power )*
power       -> unary ( "^" power )?
unary       -> ("+" | "-") unary | primary
primary     -> NUMBER
            | IDENTIFIER
            | FUNCTION_CALL
            | "(" expression ")"
FUNCTION_CALL -> (IDENTIFIER | FUNCTION) "(" [expression ("," expression)*] ")"
```

This grammar enforces:

- Multiplication/division precedence over addition/subtraction.
- Exponentiation as right-associative.
- Unary plus/minus.
- Nested parenthesized expressions and function calls.

---

## Implementation Description

Files added for Lab 6:

- `Lab6/src/tokens.py`
- `Lab6/src/lexer.py`
- `Lab6/src/ast_nodes.py`
- `Lab6/src/parser.py`
- `Lab6/src/main.py`

### 1. Token Model (`tokens.py`)

- `TokenType` is defined as an enum-like type for lexical categories.
- `Token` stores: `type`, `value`, `line`, `column`.

### 2. Regex-Based Lexer (`lexer.py`)

The lexer uses a single master regex built from named patterns. Important pattern groups:

- `FLOAT`: `\d+\.\d+`
- `INTEGER`: `\d+`
- `FUNCTION`: `\b(?:sin|cos|tan|sqrt)\b`
- `IDENTIFIER`: `[A-Za-z_][A-Za-z0-9_]*`
- operator and delimiter groups for `+ - * / ^ ( ) ,`

The tokenization loop:

1. Matches the next lexeme at current position.
2. Determines token type from the regex group name.
3. Converts numeric lexemes to `int` or `float` values.
4. Tracks line/column positions.
5. Emits `ERROR` for mismatches and always appends `EOF`.

### 3. AST Data Structures (`ast_nodes.py`)

AST node types:

- `NumberNode`
- `IdentifierNode`
- `UnaryOpNode`
- `BinaryOpNode`
- `FunctionCallNode`

These nodes form a hierarchical abstract representation of expressions.

### 4. Recursive-Descent Parser (`parser.py`)

The parser consumes token sequences and builds AST nodes according to grammar rules.

Main characteristics:

- Precedence levels split across dedicated parse functions.
- Right-associative parsing for exponentiation (`2 ^ 3 ^ 2` -> `2 ^ (3 ^ 2)`).
- Function-call parsing with variable-length argument lists.
- Positional error messages for lexical and syntax errors.

### 5. Demonstration Driver (`main.py`)

The main script runs multiple test cases and prints:

- Input expression
- Produced tokens
- AST representation (or parser error)

It includes valid expressions and invalid samples (`x @ y`, `sin(2 + )`) to demonstrate error handling.

---

## Code Snippets

### Regex Master Pattern

```python
MASTER_PATTERN = re.compile(
    "|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPECS),
    re.MULTILINE,
)
```

### Parser Entry

```python
def parse(self):
    lexical_errors = [token for token in self.tokens if token.type == TokenType.ERROR]
    if lexical_errors:
        first_error = lexical_errors[0]
        raise ParserError(
            f"Lexical error at line {first_error.line}, column {first_error.column}: {first_error.value}"
        )

    node = self._parse_expression()
    self._consume(TokenType.EOF, "Expected end of input")
    return node
```

### Right-Associative Power Rule

```python
def _parse_power(self):
    node = self._parse_unary()

    if self._current().type == TokenType.POWER:
        operator = self._advance()
        right = self._parse_power()
        node = BinaryOpNode(node, operator.value, right)

    return node
```

---

## Execution and Results

Command used:

```bash
cd Lab6/src
python3 main.py
```

Observed behavior:

1. `2 + 3 * 4` -> AST root is `BinaryOp(+)` with right branch `BinaryOp(*)`.
2. `sin(x) + cos(y)` -> function calls parsed as dedicated `FunctionCallNode` nodes.
3. `-sqrt(16) + tan(y) / 2` -> unary minus and division precedence handled correctly.
4. `2 ^ 3 ^ 2` -> parsed as right-associative exponent tree.
5. `sin(x, y + 1)` -> multi-argument function call parsed correctly.
6. `x @ y` -> lexical error reported with exact column.
7. `sin(2 + )` -> syntax error reported at unexpected token.

No editor diagnostics remained in `Lab6/src` after implementation.

---

## Difficulties Encountered

1. **Operator associativity for exponentiation**

A left-to-right implementation of power would be incorrect. The parser was adjusted to recurse on the right side for `^`.

2. **Reliable source position tracking with regex tokenization**

Because whitespace and comments are skipped, line and column tracking had to be updated consistently after each matched lexeme.

3. **Module naming collision with Python stdlib `token`**

Using `token.py` in Lab 6 conflicted with standard library imports during runtime. Renaming to `tokens.py` resolved the issue.

---

## Conclusion

Lab 6 requirements were implemented end-to-end for the Lab 3 language:

- Token categories are explicit through `TokenType`.
- Token types are identified using regular expressions.
- AST structures were defined and used.
- A functional recursive-descent parser extracts syntactic structure and reports errors.

The resulting implementation is suitable as a base for next compilation stages such as semantic checks or expression evaluation.

## References

[1] Parsing Wiki: https://en.wikipedia.org/wiki/Parsing

[2] Abstract Syntax Tree Wiki: https://en.wikipedia.org/wiki/Abstract_syntax_tree
