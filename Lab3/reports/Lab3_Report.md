# Lab 3: Lexical Analysis and Tokenization

### Course: Formal Languages & Finite Automata

### Author: Catalin Bitca

---

## Theory

**Lexical analysis** is the first phase of a compiler or interpreter, responsible for breaking down a source program (a stream of characters) into a sequence of meaningful units called **tokens** or **lexemes**. This process is typically performed by a component called a **lexer**, **scanner**, or **tokenizer**.

A **lexeme** is a sequence of characters in the source program that matches the pattern for a token. For example, in the expression `sin(3.14)`, the substrings `sin`, `(`, `3.14`, and `)` are all lexemes.

A **token** is a semantic unit represented by a token type and optional attributes. While a lexeme is just text, a token assigns a category and meaning to it. For example, the lexeme `sin` becomes the token `Token(TokenType.SIN, 'sin')`, and the lexeme `3.14` becomes `Token(TokenType.FLOAT, 3.14)`.

The **token type** categorizes lexemes into classes such as:
- Keywords (e.g., `sin`, `cos`, `sqrt`, `tan`)
- Identifiers (variable names like `x`, `var1`, `result`)
- Numeric literals (integers like `42` or floats like `3.14`)
- Operators (+, -, *, /, ^)
- Delimiters ((, ), ,)
- Special tokens (EOF for end-of-file, ERROR for invalid input)

The lexer typically uses **finite automata** to recognize patterns. For instance, recognizing a floating-point number involves:
1. Reading a sequence of digits (state transition on each digit)
2. Optionally reading a decimal point followed by more digits
3. Accepting the complete lexeme when the pattern is satisfied

The **advantages** of separating lexical analysis into a distinct phase include:
- **Simplicity**: The parser only deals with tokens, not raw characters
- **Efficiency**: Pattern recognition is optimized by the lexer
- **Maintainability**: Changes to the language's keywords or operators are localized to the lexer
- **Error Recovery**: Lexical errors can be detected and reported early

---

## Objectives

1. Understand the principles of lexical analysis and tokenization.
2. Implement a lexer capable of recognizing multiple token types including keywords, identifiers, numeric literals, and operators.
3. Handle floating-point and integer numbers, as well as trigonometric function keywords.
4. Build and test the lexer with complex mathematical expressions.
5. Demonstrate proper error handling for unexpected characters.

---

## Language Specification

The lexer recognizes a mathematical expression language with the following token types:

**Literals:**
- `INTEGER` — sequences of digits, e.g., `42`, `1000`
- `FLOAT` — integer followed by a decimal point and fractional digits, e.g., `3.14`, `2.5`

**Keywords:**
- `SIN`, `COS`, `TAN`, `SQRT` — mathematical function names

**Identifiers:**
- Sequences of alphanumeric characters and underscores starting with a letter or underscore, e.g., `x`, `var1`, `result_value`

**Operators and Delimiters:**
- `PLUS` (+), `MINUS` (-), `MULTIPLY` (*), `DIVIDE` (/), `POWER` (^)
- `LPAREN` ((), `RPAREN` ()), `COMMA` (,)

**Special Tokens:**
- `EOF` — end of input
- `ERROR` — invalid or unexpected input

Comments beginning with `#` are skipped and do not produce tokens.

---

## Implementation Description

The implementation consists of three files:

- **token.py** — defines token types and the `Token` class
- **lexer.py** — implements the `Lexer` class that performs the tokenization
- **main.py** — a test driver demonstrating the lexer on various inputs

### Token and TokenType Classes

The `Token` class encapsulates a single token with four attributes:
- **type**: The token category (from the `TokenType` enum)
- **value**: The actual lexeme or semantic value (e.g., the number `3.14` or the keyword string `'sin'`)
- **line**: The source line number (useful for error reporting)
- **column**: The column position (useful for error reporting)

The `TokenType` enum defines all possible token categories, including both terminal symbols from the language grammar and special tokens.

### Lexer Class

The `Lexer` class maintains the following state:
- **text**: The input string to be tokenized
- **pos**: Current position in the input (0-indexed)
- **line** and **column**: Current position for error reporting
- **tokens**: List of accumulated tokens

**Core Methods:**

**`current_char()` and `peek_char()`** — character inspection methods that safely return the current or lookahead character, or `None` if at the end of input.

**`advance()`** — moves to the next character and updates line and column counters. When a newline is encountered, the line counter increments and the column resets.

**`skip_whitespace()` and `skip_comment()`** — skip over insignificant input. Whitespace (spaces, tabs, newlines) is simply discarded. Comments starting with `#` are skipped until the end of the line.

**`read_number()`** — reads integer or floating-point literals. It begins by consuming all initial digits, then checks for a decimal point followed by fractional digits. If a decimal point is present, the number is tokenized as `FLOAT`; otherwise as `INTEGER`. The actual numeric value (not just the string) is stored to facilitate later evaluation.

**`read_identifier()`** — reads alphanumeric sequences starting with a letter or underscore. After extracting the identifier string, the lexer checks if it is a keyword (using a lookup dictionary). If it is, the corresponding keyword token type is returned; otherwise, it is treated as an `IDENTIFIER`.

**`tokenize()`** — the main tokenization loop. It repeatedly:
1. Skips whitespace and comments
2. Checks the current character to determine the token type
3. Calls the appropriate lexeme-reading method (for numbers and identifiers) or directly creates a token for single-character operators
4. Appends the token to the token list
5. Continues until the end of input, then appends an `EOF` token

Whenever an unexpected character is encountered, an `ERROR` token is created with a descriptive message.

### Main Driver

The `main.py` file contains test cases that exercise the lexer on various inputs:
- Simple arithmetic: `2 + 3`
- Floating-point operations: `3.14 * 2.5`
- Function calls: `sin(0.5)`, `cos(x)`
- Complex expressions: `sin(x) + cos(y) * 2.5`
- Power operations: `2 ^ 8`
- Comments: `x + 5  # comment`
- Variable names: `var1 + var_2`
- Error cases: `x @ y` (invalid character)

Each test case is executed, and all resulting tokens are printed in a readable format, demonstrating lexical analysis in action.

---

## Code Snippets

### Token Class Definition

```python
class Token:
    def __init__(self, type_, value, line, column):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column
    
    def __repr__(self):
        return f"Token({self.type.name}, {repr(self.value)}, {self.line}, {self.column})"
```

### Number Recognition

```python
def read_number(self):
    start_pos = self.pos
    start_col = self.column
    
    while self.current_char() and self.current_char().isdigit():
        self.advance()
    
    if self.current_char() == '.' and self.peek_char() and self.peek_char().isdigit():
        self.advance()
        while self.current_char() and self.current_char().isdigit():
            self.advance()
        value = float(self.text[start_pos:self.pos])
        return Token(TokenType.FLOAT, value, self.line, start_col)
    else:
        value = int(self.text[start_pos:self.pos])
        return Token(TokenType.INTEGER, value, self.line, start_col)
```

### Identifier and Keyword Recognition

```python
def read_identifier(self):
    start_pos = self.pos
    start_col = self.column
    
    while self.current_char() and (self.current_char().isalnum() or self.current_char() == '_'):
        self.advance()
    
    identifier = self.text[start_pos:self.pos]
    
    if identifier in self.KEYWORDS:
        return Token(self.KEYWORDS[identifier], identifier, self.line, start_col)
    else:
        return Token(TokenType.IDENTIFIER, identifier, self.line, start_col)
```

### Main Tokenization Loop

```python
def tokenize(self):
    while self.pos < len(self.text):
        self.skip_whitespace()
        
        if self.current_char() is None:
            break
        
        if self.current_char() == '#':
            self.skip_comment()
            continue
        
        char = self.current_char()
        col = self.column
        
        if char.isdigit():
            self.tokens.append(self.read_number())
        elif char.isalpha() or char == '_':
            self.tokens.append(self.read_identifier())
        elif char == '+':
            self.tokens.append(Token(TokenType.PLUS, '+', self.line, col))
            self.advance()
        # ... similar handling for other operators
        else:
            self.error(f"Unexpected character: {char}")
            self.advance()
    
    self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
    return self.tokens
```

---

## Testing and Results

The lexer has been tested on a variety of inputs spanning different aspects of the language:

1. **Basic Arithmetic**: `2 + 3` → Tokens: `INTEGER(2)`, `PLUS`, `INTEGER(3)`, `EOF`
2. **Floating-Point Operations**: `3.14 * 2.5` → Correctly tokenizes both floats and the multiply operator
3. **Function Calls**: `sin(0.5)` → Tokens: `SIN`, `LPAREN`, `FLOAT(0.5)`, `RPAREN`, `EOF`
4. **Variables**: `x + y` → Tokens: `IDENTIFIER('x')`, `PLUS`, `IDENTIFIER('y')`, `EOF`
5. **Complex Expressions**: `sin(x) + cos(y) * 2.5` → Correctly tokenizes nested functions with mixed operators
6. **Power Operations**: `2 ^ 8` → Correctly recognizes the power operator
7. **Comments**: `x + 5  # comment` → Comments are properly skipped
8. **Error Handling**: `x @ y` → `ERROR` token generated for unexpected character `@`

All test cases demonstrate that the lexer correctly identifies lexemes and assigns them appropriate token types, properly maintains position information for error reporting, and gracefully handles invalid input.

---

## Conclusion

This laboratory implements a functional lexer for a mathematical expression language, successfully demonstrating the principles of lexical analysis. The lexer correctly tokenizes complex expressions with trigonometric functions, floating-point numbers, variables, and various operators. The separation of token types allows for clear downstream processing by a parser or interpreter, and the integrated error handling provides meaningful feedback for malformed input.
