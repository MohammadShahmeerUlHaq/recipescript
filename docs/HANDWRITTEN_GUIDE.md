# Handwritten Artifacts Guide for RecipeScript Compiler

## ⚠️ IMPORTANT: These artifacts MUST be handwritten

According to project requirements, you must submit handwritten design documents for lexical, syntax, and semantic phases. This file guides you on what to create.

---

## 1. Lexical Analysis Artifacts (HANDWRITTEN REQUIRED)

### 1.1 DFA for Token Recognition

**Draw a Deterministic Finite Automaton (DFA) for:**

#### Example 1: Identifier Recognition
```
States: q0 (start), q1 (accepting)
Alphabet: [a-z], [A-Z], [0-9], _

Transitions:
q0 --[a-z,A-Z,_]--> q1
q1 --[a-z,A-Z,0-9,_]--> q1
```

Draw this as a state diagram with circles for states and arrows for transitions.

#### Example 2: Number Recognition (Integer and Float)
```
States: q0 (start), q1 (integer), q2 (decimal point), q3 (float)

q0 --[0-9]--> q1 (accepting)
q1 --[0-9]--> q1
q1 --[.]--> q2
q2 --[0-9]--> q3 (accepting)
q3 --[0-9]--> q3
```

#### Example 3: Keyword "ingredient"
Draw a DFA that recognizes the exact sequence: i-n-g-r-e-d-i-e-n-t

### 1.2 Transition Table

Create a table for identifier recognition:

```
| State | [a-z,A-Z,_] | [0-9] | Other |
|-------|-------------|-------|-------|
| q0    | q1          | -     | error |
| q1    | q1          | q1    | accept|
```

### 1.3 Regular Expressions

Write regular expressions for:
- Identifier: `[a-zA-Z_][a-zA-Z0-9_]*`
- Integer: `[0-9]+`
- Float: `[0-9]+\.[0-9]+`
- String: `"[^"]*"`
- Comment: `#[^\n]*`

---

## 2. Syntax Analysis Artifacts (HANDWRITTEN REQUIRED)

### 2.1 Parse Tree Derivations (Minimum 2 Required)

#### Parse Tree 1: Simple Declaration
```
Code: ingredient flour = 2 cups;

Draw parse tree showing:
<statement>
    |
<declaration>
    |
<type> <identifier> = <value>
    |       |           |
ingredient flour    <number> <unit>
                       |       |
                       2      cups
```

#### Parse Tree 2: Mix Operation
```
Code: mix flour with sugar with butter;

Draw parse tree showing:
<statement>
    |
<operation>
    |
<mix_operation>
    |
mix <ingredient_list>
        |
    <identifier> with <ingredient_list>
        |                |
      flour          <identifier> with <identifier>
                         |                |
                       sugar            butter
```

#### Parse Tree 3: When Statement (Conditional)
```
Code: when current < target then { heat oven to 350 F; }

Draw complete parse tree with:
- <when_statement>
- <condition>
- <comparison>
- <then_body>
- <statement_list>
```

#### Parse Tree 4: Repeat Statement
```
Code: repeat 3 times { mix dough; }

Draw parse tree showing loop structure
```

### 2.2 Leftmost Derivation

Show step-by-step leftmost derivation for:
```
ingredient flour = 2 cups;
```

Steps:
```
<program>
=> <statement_list>
=> <statement>
=> <declaration> ;
=> <type> <identifier> = <value> ;
=> ingredient <identifier> = <value> ;
=> ingredient flour = <value> ;
=> ingredient flour = <number> <unit> ;
=> ingredient flour = 2 <unit> ;
=> ingredient flour = 2 cups ;
```

### 2.3 Grammar Rules (BNF)

Write out key grammar rules by hand:
```
<program> ::= <statement_list>
<statement> ::= <declaration> ";" | <operation> ";"
<declaration> ::= <type> <identifier> "=" <value>
<type> ::= "ingredient" | "time" | "temp" | "quantity"
<value> ::= <number> <unit> | <number>
```

---

## 3. Semantic Analysis Artifacts (HANDWRITTEN REQUIRED)

### 3.1 Symbol Table Example

Create a symbol table for this code:
```
ingredient flour = 2 cups;
temp oven = 350 F;
ingredient sugar = 1 cups;
```

Draw table:
```
+-------------+------------+-------+------+
| Name        | Type       | Scope | Line |
+-------------+------------+-------+------+
| flour       | ingredient | 0     | 1    |
| oven        | temp       | 0     | 2    |
| sugar       | ingredient | 0     | 3    |
+-------------+------------+-------+------+
```

### 3.2 Symbol Table with Scopes

Show scope handling for:
```
ingredient flour = 2 cups;
repeat 3 times {
    ingredient temp_flour = 1 cups;
    mix temp_flour;
}
```

Draw table showing scope levels:
```
+-------------+------------+-------+------+
| Name        | Type       | Scope | Line |
+-------------+------------+-------+------+
| flour       | ingredient | 0     | 1    |
| temp_flour  | ingredient | 1     | 3    |
+-------------+------------+-------+------+

After exiting repeat block, temp_flour is removed.
```

### 3.3 Type Checking Examples

Show type checking for:

**Example 1: Valid**
```
ingredient flour = 2 cups;  ✓ Type: ingredient, Value: 2 cups
```

**Example 2: Invalid**
```
temp oven = 600 F;  ✗ Error: Temperature out of range (0-500F)
```

**Example 3: Undeclared Variable**
```
mix flour with sugar;  ✗ Error: 'sugar' not declared
```

### 3.4 Semantic Rules

Write out semantic rules:
1. Variables must be declared before use
2. Temperature range: 0-500°F or 0-260°C
3. Time and quantity must be positive
4. Only ingredients can be mixed
5. Type compatibility in operations

---

## 4. Intermediate Code Examples (HANDWRITTEN OPTIONAL)

### 4.1 Three-Address Code (TAC)

Show TAC for:
```
ingredient flour = 2 cups;
ingredient sugar = 1 cups;
mix flour with sugar;
```

TAC:
```
1: flour = 2 cups
2: sugar = 1 cups
3: mix flour, sugar
```

### 4.2 TAC for Control Flow

Show TAC for:
```
when current < target then {
    heat oven to 350 F;
}
```

TAC:
```
1: t0 = current < target
2: if_false t0 goto L1
3: heat oven to 350 fahrenheit
4: L1:
```

---

## 5. Optimization Examples (HANDWRITTEN OPTIONAL)

### 5.1 Constant Folding

**Before:**
```
t0 = 2 + 3
result = t0
```

**After:**
```
result = 5
```

### 5.2 Dead Code Elimination

**Before:**
```
t0 = 10
t1 = 20
result = t0
```

**After:**
```
t0 = 10
result = t0
```
(t1 is removed as it's never used)

---

## Submission Checklist

### Required Handwritten Artifacts:

- [ ] **Lexical Phase:**
  - [ ] DFA for identifier recognition
  - [ ] DFA for number recognition
  - [ ] Transition table
  - [ ] Regular expressions for tokens

- [ ] **Syntax Phase:**
  - [ ] Parse tree for declaration statement
  - [ ] Parse tree for mix operation
  - [ ] Leftmost derivation example
  - [ ] Grammar rules (BNF)

- [ ] **Semantic Phase:**
  - [ ] Symbol table without scopes
  - [ ] Symbol table with scope example
  - [ ] Type checking examples
  - [ ] Semantic error examples

### Optional (but recommended):
- [ ] TAC generation examples
- [ ] Optimization examples
- [ ] Control flow diagrams

---

## Tips for Creating Handwritten Artifacts

1. **Use clean, lined paper**
2. **Draw clearly with pencil first, then pen**
3. **Label all states, transitions, and nodes**
4. **Use different colors for clarity**
5. **Add annotations explaining your diagrams**
6. **Scan or photograph clearly**
7. **Ensure all text is readable**

---

## Grading Criteria

Your handwritten artifacts will be evaluated on:
- **Correctness**: Accurate representation of concepts
- **Completeness**: All required elements present
- **Clarity**: Easy to read and understand
- **Detail**: Sufficient annotations and labels
- **Presentation**: Neat and organized

---

## Example Layout

For each artifact, use this format:

```
┌─────────────────────────────────────┐
│ Artifact Title                      │
│ (e.g., "DFA for Identifier")        │
├─────────────────────────────────────┤
│                                     │
│  [Your diagram/table here]          │
│                                     │
├─────────────────────────────────────┤
│ Explanation:                        │
│ [Brief description of what this     │
│  shows and why it's important]      │
└─────────────────────────────────────┘
```

---

Good luck with your handwritten artifacts! Remember, these demonstrate your understanding of compiler theory, so take your time and be thorough.
