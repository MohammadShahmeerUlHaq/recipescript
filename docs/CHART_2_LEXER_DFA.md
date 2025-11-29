# CHART PAPER 2: LEXICAL ANALYZER (DFA)
## RecipeScript - Deterministic Finite Automata for Tokens

---

## DFA 1: IDENTIFIER RECOGNITION

**Pattern:** `[a-zA-Z_][a-zA-Z0-9_]*`

**States:**
- q0 = Start state
- q1 = Accepting state (valid identifier)

**Transitions:**
```
State q0:
  [a-z, A-Z, _] → q1
  [other] → ERROR

State q1 (ACCEPT):
  [a-z, A-Z, 0-9, _] → q1
  [other] → ACCEPT & RETURN
```

**Diagram:**
```
        [a-zA-Z_]
    ┌─────────────┐
    │             ↓
  (q0) ────────> ((q1))
                  │ ↺ [a-zA-Z0-9_]
                  │
                  └──→ ACCEPT
```

**Examples:**
- `flour` ✓
- `sugar_2` ✓
- `_temp` ✓
- `2flour` ✗ (starts with digit)

---

## DFA 2: NUMBER RECOGNITION

**Pattern:** `[0-9]+(\.[0-9]+)?`

**States:**
- q0 = Start state
- q1 = Integer part (accepting)
- q2 = Decimal point seen
- q3 = Decimal part (accepting)

**Transitions:**
```
State q0:
  [0-9] → q1
  [other] → ERROR

State q1 (ACCEPT - INTEGER):
  [0-9] → q1
  [.] → q2
  [other] → ACCEPT & RETURN

State q2:
  [0-9] → q3
  [other] → ERROR

State q3 (ACCEPT - FLOAT):
  [0-9] → q3
  [other] → ACCEPT & RETURN
```

**Diagram:**
```
        [0-9]           [.]           [0-9]
  (q0) ────────> ((q1)) ────────> (q2) ────────> ((q3))
                  │ ↺ [0-9]                       │ ↺ [0-9]
                  │                                │
                  └──→ ACCEPT (INT)                └──→ ACCEPT (FLOAT)
```

**Examples:**
- `42` ✓ (integer)
- `3.14` ✓ (float)
- `0.5` ✓ (float)
- `.5` ✗ (no leading digit)
- `5.` ✗ (no trailing digit)

---

## DFA 3: STRING LITERAL RECOGNITION

**Pattern:** `"[^"]*"`

**States:**
- q0 = Start state
- q1 = Inside string
- q2 = Accepting state (closing quote)

**Transitions:**
```
State q0:
  ["] → q1
  [other] → ERROR

State q1:
  ["] → q2
  [any char except "] → q1
  [EOF] → ERROR (unterminated string)

State q2 (ACCEPT):
  → ACCEPT & RETURN
```

**Diagram:**
```
        ["]              [any except "]         ["]
  (q0) ────────> (q1) ─────────────────> ((q2))
                  │ ↺                      
                  │                        
                  └──→ ERROR (EOF)
```

**Examples:**
- `"Mix well"` ✓
- `"Preheat oven"` ✓
- `"Hello` ✗ (unterminated)

---

## DFA 4: OPERATOR RECOGNITION

**Pattern:** `=|==|!=|<=|>=|<|>|+|-|*|/`

**States:**
- q0 = Start state
- q1 = Single char operator (accepting)
- q2 = Two char operator (accepting)

**Transitions:**
```
State q0:
  [=] → q1
  [!] → q1
  [<] → q1
  [>] → q1
  [+, -, *, /] → q2
  [other] → ERROR

State q1 (ACCEPT - SINGLE):
  [=] → q2 (for ==, !=, <=, >=)
  [other] → ACCEPT & RETURN

State q2 (ACCEPT - COMPLETE):
  → ACCEPT & RETURN
```

**Diagram:**
```
        [=!<>]          [=]
  (q0) ────────> ((q1)) ────────> ((q2))
    │                    │
    │ [+-*/]             └──→ ACCEPT (=, !, <, >)
    │
    └────────────────────────────> ((q2))
                                    │
                                    └──→ ACCEPT (+, -, *, /)
```

**Examples:**
- `==` ✓ (equality)
- `!=` ✓ (not equal)
- `<=` ✓ (less or equal)
- `+` ✓ (addition)
- `=` ✓ (assignment)

---

## DFA 5: KEYWORD vs IDENTIFIER

**Strategy:** Identifier DFA + Keyword Lookup Table

**Process:**
1. Use Identifier DFA to recognize pattern
2. Check if recognized string is in keyword table
3. If YES → Return KEYWORD token
4. If NO → Return IDENTIFIER token

**Keyword Table:**
```
ingredient, time, temp, quantity, text,
mix, heat, wait, serve, display, add, scale, remove,
repeat, foreach, when, then, else, times, in,
recipe, return, returns,
input, to, with, for, at, from, by,
cups, tbsp, tsp, ml, oz, grams, lbs,
F, C, minutes, seconds, hours
```

**Algorithm:**
```
1. Run Identifier DFA
2. If ACCEPT:
     lexeme = captured_string
     if lexeme in KEYWORD_TABLE:
         return Token(KEYWORD, lexeme)
     else:
         return Token(IDENTIFIER, lexeme)
3. If REJECT:
     return ERROR
```

---

## DFA 6: COMMENT RECOGNITION

**Pattern:** `#[^\n]*`

**States:**
- q0 = Start state
- q1 = Inside comment (accepting)

**Transitions:**
```
State q0:
  [#] → q1
  [other] → ERROR

State q1 (ACCEPT):
  [\n] → ACCEPT & RETURN
  [EOF] → ACCEPT & RETURN
  [any other char] → q1
```

**Diagram:**
```
        [#]              [any except \n]        [\n or EOF]
  (q0) ────────> ((q1)) ─────────────────> ACCEPT
                  │ ↺                      
```

**Examples:**
- `# This is a comment` ✓
- `# Mix ingredients` ✓

---

## COMPLETE TOKEN TYPES

```
1. KEYWORD          - Reserved words
2. IDENTIFIER       - Variable names
3. NUMBER           - Integer or float
4. STRING           - Text literals
5. OPERATOR         - =, +, -, *, /, ==, !=, <, >, <=, >=
6. DELIMITER        - ;, ,, (, ), {, }
7. UNIT             - cups, grams, F, minutes, etc.
8. COMMENT          - # comments
9. EOF              - End of file
10. ERROR           - Invalid token
```

---

## LEXER ALGORITHM

```
1. Initialize: position = 0, tokens = []

2. While not EOF:
   a. Skip whitespace
   b. Try each DFA in priority order:
      - Comment DFA
      - Number DFA
      - String DFA
      - Identifier/Keyword DFA
      - Operator DFA
      - Delimiter (single char)
   c. If match found:
      - Create token
      - Add to token list
      - Advance position
   d. If no match:
      - Report lexical error
      - Skip character
      - Continue

3. Add EOF token

4. Return token list
```

---

## TRANSITION TABLE EXAMPLE (Identifier)

```
┌───────┬─────────┬─────────┬─────────┬─────────┐
│ State │ [a-zA-Z]│   [_]   │ [0-9]   │  other  │
├───────┼─────────┼─────────┼─────────┼─────────┤
│  q0   │   q1    │   q1    │  ERROR  │  ERROR  │
│  q1   │   q1    │   q1    │   q1    │ ACCEPT  │
└───────┴─────────┴─────────┴─────────┴─────────┘
```

---
