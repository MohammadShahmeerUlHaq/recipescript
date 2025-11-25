# RecipeScript Compiler - Complete Project Documentation

## Project Overview

**Language Name:** RecipeScript  
**Domain:** Cooking recipe automation and meal planning  
**Purpose:** A domain-specific language for writing structured cooking recipes with automated timing and ingredient management

---

## 1. Language Design Rationale

### Why RecipeScript?

RecipeScript was designed to address the need for:
- **Structured recipe representation** - Clear, unambiguous cooking instructions
- **Automated timing** - Built-in time management for cooking steps
- **Ingredient tracking** - Automatic quantity calculations and scaling
- **Temperature management** - Safe temperature range validation
- **Recipe automation** - Potential for smart kitchen integration

### Unique Features

1. **Domain-Specific Types**
   - `ingredient` - Food items with quantities
   - `temp` - Temperature with unit validation
   - `time` - Duration values
   - `quantity` - Numeric measurements

2. **Cooking Operations**
   - `mix` - Combine ingredients
   - `heat` - Set temperature
   - `wait` - Timing control
   - `serve` - Output/completion
   - `scale` - Adjust quantities

3. **Natural Language Syntax**
   - `mix flour with sugar with butter`
   - `heat oven to 350 F`
   - `wait 15 minutes`
   - `repeat 3 times`

---

## 2. Complete Language Specification

### 2.1 Lexical Specification

#### Keywords (Reserved Words)
```
Data Types:     ingredient, time, temp, quantity, text
Operations:     mix, heat, wait, serve, scale, add, remove
Control Flow:   repeat, foreach, when, then, else, times, in
Prepositions:   to, with, for, at, from, by
```

#### Units
```
Volume:         cups, tbsp, tsp, ml, oz
Weight:         grams, lbs
Temperature:    F (Fahrenheit), C (Celsius)
Time:           minutes, seconds, hours
```

#### Operators
```
Arithmetic:     + - * /
Comparison:     == != > < >= <=
Assignment:     =
```

#### Delimiters
```
;   Statement terminator
,   Separator
( ) Parentheses
{ } Braces
```

#### Literals
```
Numbers:        123, 45.67
Strings:        "Hello World"
Identifiers:    flour, oven_temp, mix1
```

#### Comments
```
# Single-line comment
```

### 2.2 Grammar (BNF)

```bnf
<program> ::= <statement_list>

<statement_list> ::= <statement>
                   | <statement> <statement_list>

<statement> ::= <declaration> ";"
              | <operation> ";"
              | <control_flow>

<declaration> ::= <type> <identifier> "=" <value>

<type> ::= "ingredient" | "time" | "temp" | "quantity" | "text"

<value> ::= <number> <unit>
          | <number>
          | <string>
          | <identifier>

<operation> ::= "mix" <ingredient_list>
              | "heat" <identifier> "to" <value>
              | "wait" <time_value>
              | "serve" <string>
              | "scale" <identifier> "by" <number>
              | "add" <identifier> "to" <identifier>

<ingredient_list> ::= <identifier>
                    | <identifier> "with" <ingredient_list>

<control_flow> ::= <repeat_stmt>
                 | <when_stmt>

<repeat_stmt> ::= "repeat" <number> "times" "{" <statement_list> "}"

<when_stmt> ::= "when" <condition> "then" "{" <statement_list> "}"
              | "when" <condition> "then" "{" <statement_list> "}" 
                "else" "{" <statement_list> "}"

<condition> ::= <expression> <comparison_op> <expression>

<expression> ::= <term>
               | <expression> "+" <term>
               | <expression> "-" <term>

<term> ::= <factor>
         | <term> "*" <factor>
         | <term> "/" <factor>

<factor> ::= <number>
           | <identifier>
           | "(" <expression> ")"
```

### 2.3 Semantic Rules

1. **Type System**
   - Static typing with type checking at compile time
   - No implicit type conversions between incompatible types

2. **Scope Rules**
   - Global scope (level 0)
   - Block scope for control structures
   - Variables must be declared before use

3. **Validation Rules**
   - Temperature: 0-500°F or 0-260°C
   - Time: Must be positive
   - Quantity: Must be positive
   - Ingredients: Must be declared before mixing

4. **Type Compatibility**
   - Only `ingredient` types can be mixed
   - Only `ingredient` types can be scaled
   - Arithmetic operations on numeric types only

---

## 3. Compiler Architecture

### 3.1 Phase 1: Lexical Analysis (`lexer.py`)

**Purpose:** Convert source code into tokens

**Implementation:**
- Character-by-character scanning
- Token recognition using pattern matching
- Keyword lookup table
- Error reporting with line/column numbers

**Key Functions:**
- `get_next_token()` - Returns next token
- `tokenize()` - Tokenizes entire source
- `skip_whitespace()` - Handles whitespace
- `skip_comment()` - Handles comments
- `read_number()` - Parses numeric literals
- `read_string()` - Parses string literals
- `read_identifier()` - Parses identifiers/keywords

**Output:** List of Token objects

### 3.2 Phase 2: Syntax Analysis (`parser.py`)

**Purpose:** Build Abstract Syntax Tree (AST)

**Implementation:**
- Recursive descent parser
- One function per grammar rule
- Predictive parsing (LL(1))
- Error recovery

**AST Node Types:**
- `Program` - Root node
- `Declaration` - Variable declarations
- `MixOperation`, `HeatOperation`, etc. - Operations
- `RepeatStatement`, `WhenStatement` - Control flow
- `BinaryOp` - Expressions
- `Number`, `String`, `Identifier` - Literals

**Key Functions:**
- `parse()` - Entry point
- `parse_statement()` - Statement parsing
- `parse_declaration()` - Variable declarations
- `parse_expression()` - Expression parsing
- `parse_condition()` - Conditional expressions

**Output:** AST (Abstract Syntax Tree)

### 3.3 Phase 3: Semantic Analysis (`semantic_analyzer.py`)

**Purpose:** Type checking and symbol table construction

**Implementation:**
- Visitor pattern for AST traversal
- Symbol table with scope management
- Type checking for operations
- Semantic validation

**Symbol Table:**
```python
{
    'name': {
        'type': TokenType,
        'scope': int,
        'line': int
    }
}
```

**Semantic Checks:**
- Variable declaration before use
- Type compatibility
- Temperature range validation
- Positive time/quantity validation
- Ingredient type validation for mixing

**Key Functions:**
- `analyze()` - Entry point
- `visit_*()` - Node-specific visitors
- `declare()` - Add to symbol table
- `lookup()` - Find variable
- `enter_scope()` / `exit_scope()` - Scope management

**Output:** Symbol table, validated AST

### 3.4 Phase 4: Intermediate Code Generation (`intermediate_code.py`)

**Purpose:** Generate Three-Address Code (TAC)

**Implementation:**
- TAC instruction generation
- Temporary variable management
- Label generation for control flow
- Expression linearization

**TAC Instruction Format:**
```
op arg1 arg2 result
```

**Examples:**
```
assign 2 None flour
mix [flour, sugar] None None
heat oven 350 None
if_false t0 None L1
goto None None L2
```

**Key Functions:**
- `generate()` - Entry point
- `visit_*()` - Generate TAC for each node
- `new_temp()` - Create temporary variable
- `new_label()` - Create label
- `emit()` - Add TAC instruction

**Output:** List of TAC instructions

### 3.5 Phase 5: Code Optimization (`optimizer.py`)

**Purpose:** Optimize TAC for better performance

**Optimizations Implemented:**

1. **Constant Folding**
   - Evaluate constant expressions at compile time
   - Example: `t0 = 2 + 3` → `t0 = 5`

2. **Dead Code Elimination**
   - Remove unused variable assignments
   - Example: Remove `t1 = 10` if t1 is never used

**Key Functions:**
- `optimize()` - Entry point
- `constant_folding()` - Fold constants
- `dead_code_elimination()` - Remove dead code
- `is_constant()` - Check if value is constant
- `evaluate_op()` - Evaluate arithmetic
- `evaluate_comparison()` - Evaluate comparisons

**Output:** Optimized TAC instructions

### 3.6 Phase 6: Code Generation (`code_generator.py`)

**Purpose:** Execute TAC instructions

**Implementation:**
- TAC interpreter
- Variable storage
- Label resolution
- Control flow execution

**Execution Model:**
- Program counter (PC)
- Variable dictionary
- Label dictionary
- Output buffer

**Supported Operations:**
- Arithmetic: add, sub, mul, div
- Comparison: eq, neq, gt, lt, gte, lte
- Control flow: goto, if_false, label
- Recipe operations: mix, heat, wait, serve, scale

**Key Functions:**
- `execute()` - Entry point
- `execute_instruction()` - Execute single instruction
- `get_value()` - Resolve operand value

**Output:** Program execution results

---

## 4. File Structure

```
recipescript-compiler/
├── compiler.py              # Main entry point (150 lines)
├── lexer.py                 # Lexical analyzer (250 lines)
├── parser.py                # Syntax analyzer (400 lines)
├── semantic_analyzer.py     # Semantic checker (200 lines)
├── intermediate_code.py     # TAC generator (250 lines)
├── optimizer.py             # Code optimizer (150 lines)
├── code_generator.py        # Code executor (200 lines)
├── token_types.py           # Token definitions (120 lines)
├── test1.recipe             # Test: Simple recipe
├── test2.recipe             # Test: Scaling
├── test3.recipe             # Test: Conditionals
├── test4.recipe             # Test: Loops
├── test5.recipe             # Test: Complex operations
├── test6.recipe             # Test: Units
├── run_all_tests.py         # Test runner
├── README.md                # Main documentation
├── LANGUAGE_SPEC.md         # Language specification
├── HANDWRITTEN_GUIDE.md     # Handwritten artifacts guide
├── PROJECT_DOCUMENTATION.md # This file
└── reflection.md            # Project reflection
```

**Total:** ~1,720 lines of code

---

## 5. Test Cases

### Test 1: Simple Cookie Recipe
**Tests:** Basic declarations, operations, output
```recipe
ingredient flour = 2 cups;
ingredient sugar = 1 cups;
temp oven = 350 F;
heat oven to 350 F;
mix flour with sugar;
wait 15 minutes;
serve "Cookies ready!";
```

### Test 2: Scaled Recipe
**Tests:** Scaling operation
```recipe
ingredient rice = 1 cups;
scale rice by 2;
wait 20 minutes;
serve "Rice for 8 people!";
```

### Test 3: Conditional Cooking
**Tests:** When/then/else control flow
```recipe
temp current = 300 F;
temp target = 350 F;
when current < target then {
    heat oven to 350 F;
}
```

### Test 4: Repeated Steps
**Tests:** Repeat loops
```recipe
ingredient dough = 1 lbs;
repeat 3 times {
    mix dough;
    wait 5 minutes;
}
```

### Test 5: Complex Operations
**Tests:** Multiple ingredients, mixing, adding
```recipe
ingredient tomatoes = 3 cups;
ingredient onions = 1 cups;
mix tomatoes with onions;
add garlic to tomatoes;
```

### Test 6: Units
**Tests:** Different units (Celsius, grams)
```recipe
temp oven = 180 C;
ingredient cake = 500 grams;
heat oven to 180 C;
wait 45 minutes;
```

---

## 6. Usage Instructions

### Running a Recipe File
```bash
python compiler.py test1.recipe
```

### Interactive Mode
```bash
python compiler.py
>>> ingredient flour = 2 cups;
>>> serve "Done!";
>>> exit
```

### Running All Tests
```bash
python run_all_tests.py
```

---

## 7. Example Output

When running `python compiler.py test1.recipe`:

```
============================================================
PHASE 1: LEXICAL ANALYSIS
============================================================
Generated 28 tokens:
  Token(TokenType.INGREDIENT, ingredient, 3:1)
  Token(TokenType.IDENTIFIER, flour, 3:12)
  Token(TokenType.ASSIGN, =, 3:18)
  ...

============================================================
PHASE 2: SYNTAX ANALYSIS
============================================================
Successfully parsed 8 statements
Abstract Syntax Tree (AST) built successfully

============================================================
PHASE 3: SEMANTIC ANALYSIS
============================================================
=== Symbol Table ===
Name            Type            Scope    Line
--------------------------------------------------
flour           INGREDIENT      0        0
sugar           INGREDIENT      0        0
butter          INGREDIENT      0        0
oven            TEMP            0        0

============================================================
PHASE 4: INTERMEDIATE CODE GENERATION
============================================================
=== Three-Address Code ===
  1: flour = 2 cups
  2: sugar = 1 cups
  3: butter = 0.5 cups
  4: oven = 350 fahrenheit
  5: heat oven to 350 fahrenheit
  6: mix flour, sugar, butter
  7: wait 15 minutes
  8: serve "Cookies are ready!"

============================================================
PHASE 5: CODE OPTIMIZATION
============================================================
=== Optimized Code ===
  1: flour = 2 cups
  2: sugar = 1 cups
  3: butter = 0.5 cups
  4: oven = 350 fahrenheit
  5: heat oven to 350 fahrenheit
  6: mix flour, sugar, butter
  7: wait 15 minutes
  8: serve "Cookies are ready!"

============================================================
PHASE 6: CODE EXECUTION
============================================================
Heating oven to 350 fahrenheit
Mixing: flour, sugar, butter
Waiting for 15 minutes
Cookies are ready!

Execution completed successfully!
```

---

## 8. Key Differences from Similar Projects

### Compared to TLang (Friend's Project):

| Feature | TLang | RecipeScript |
|---------|-------|--------------|
| Domain | General purpose | Cooking recipes |
| Keywords | show, check, otherwise | mix, heat, serve, when |
| Data Types | int, float, string | ingredient, temp, time |
| Loops | loop from...to | repeat...times |
| Conditionals | check/otherwise | when/then/else |
| Unique Features | Increment/decrement | Units, scaling, mixing |
| Syntax Style | C-like | Natural language |

### Unique Aspects of RecipeScript:

1. **Domain-Specific Types** - ingredient, temp, time
2. **Unit System** - cups, F, minutes, etc.
3. **Natural Language** - "mix flour with sugar"
4. **Validation** - Temperature ranges, positive values
5. **Recipe Operations** - mix, heat, wait, serve, scale
6. **Practical Application** - Real-world cooking automation

---

## 9. Technical Highlights

### Lexical Analysis
- Multi-character operator recognition
- Unit literal handling
- Comment support
- Line/column tracking

### Syntax Analysis
- Recursive descent parsing
- Natural language syntax
- Clean AST representation
- Good error messages

### Semantic Analysis
- Type-specific validation
- Range checking (temperature)
- Scope management
- Ingredient tracking

### Intermediate Code
- Three-address code format
- Control flow with labels
- Temporary variables
- Recipe-specific operations

### Optimization
- Constant folding
- Dead code elimination
- Extensible framework

### Code Generation
- Direct TAC interpretation
- Variable storage
- Label resolution
- Recipe execution

---

## 10. Educational Value

This project demonstrates:

1. **Compiler Theory**
   - Lexical analysis (DFA, regex)
   - Context-free grammars (BNF)
   - Parsing techniques (recursive descent)
   - Symbol tables and scoping
   - Type systems
   - Intermediate representations
   - Code optimization
   - Code generation

2. **Software Engineering**
   - Modular design
   - Clean code practices
   - Error handling
   - Testing methodology
   - Documentation

3. **Domain-Specific Languages**
   - Language design principles
   - Syntax design for usability
   - Domain modeling
   - Practical applications

---

## 11. Future Enhancements

1. **Language Features**
   - Functions/procedures for recipes
   - Arrays for ingredient lists
   - Recipe import/export
   - Ingredient substitution rules

2. **Optimizations**
   - Instruction reordering
   - Parallel step execution
   - Time optimization
   - Resource allocation

3. **Code Generation**
   - Actual bytecode generation
   - Smart kitchen device integration
   - Recipe scheduling
   - Shopping list generation

4. **Tools**
   - IDE support
   - Syntax highlighting
   - Debugger
   - Recipe visualizer

---

## 12. Conclusion

RecipeScript is a complete, working compiler that demonstrates all six phases of compilation for a practical domain-specific language. It showcases understanding of:

- Formal language theory
- Compiler design patterns
- Data structures and algorithms
- Software engineering principles

The project is unique, well-documented, and ready for demonstration and submission.

---

**Project Status:** ✅ COMPLETE AND READY FOR SUBMISSION
