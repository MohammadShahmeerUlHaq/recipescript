# RecipeScript Language Specification

## 1. Overview

RecipeScript is a domain-specific language for cooking recipe automation. It provides structured syntax for defining ingredients, cooking operations, timing, and serving instructions.

## 2. Lexical Specification

### 2.1 Keywords
```
Data Types: ingredient, time, temp, quantity, text
Operations: mix, heat, wait, serve, scale, add, remove
Control Flow: repeat, foreach, when, then, else, times, in
Input/Output: input
Prepositions: to, with, for, at, from, by
Units (Volume): cups, tbsp, tsp, ml, oz
Units (Weight): grams, lbs
Units (Temperature): F, C
Units (Time): minutes, seconds, hours
```

### 2.2 Operators
```
=   Assignment
+   Addition
-   Subtraction
*   Multiplication
/   Division
==  Equal
!=  Not equal
>   Greater than
<   Less than
>=  Greater or equal
<=  Less or equal
```

### 2.3 Delimiters
```
;   Statement terminator
,   Separator
( ) Parentheses
{ } Braces
```

### 2.4 Literals

**Numeric Literals:**
```
Integer: [0-9]+
Float: [0-9]+\.[0-9]+
Examples: 2, 3.5, 100, 0.25
```

**Text Literals:**
```
"[characters]*"
Examples: "Mix well", "Preheat oven"
```

**Unit Literals:**
```
cups, tbsp, tsp, grams, ml, oz, lbs
F, C (temperature)
minutes, seconds, hours (time)
```

### 2.5 Identifiers
```
[a-zA-Z_][a-zA-Z0-9_]*
Examples: flour, sugar, oven_temp, mix1
```

### 2.6 Comments
```
# This is a single-line comment
```

## 3. Syntax Specification (BNF Grammar)

```bnf
<program> ::= <statement_list>

<statement_list> ::= <statement>
                   | <statement> <statement_list>

<statement> ::= <input_stmt> ";"
              | <declaration> ";"
              | <operation> ";"
              | <control_flow>
              | <comment>

<input_stmt> ::= "input" <identifier>

<declaration> ::= <type> <identifier> "=" <value>

<type> ::= "ingredient" | "time" | "temp" | "quantity" | "text"

<value> ::= <expression> <unit>
          | <expression>
          | <text_literal>
          | <identifier>
          | <identifier>

<unit> ::= "cups" | "tbsp" | "tsp" | "grams" | "ml" | "oz" | "lbs"
         | "F" | "C"
         | "minutes" | "seconds" | "hours"

<operation> ::= "mix" <ingredient_list>
              | "heat" <identifier> "to" <value>
              | "wait" <time_value>
              | "serve" <text_literal>
              | "display" <identifier>
              | "add" <identifier> "to" <identifier>
              | "scale" <identifier> "by" <number>

<ingredient_list> ::= <identifier>
                    | <identifier> "with" <ingredient_list>

<control_flow> ::= <repeat_stmt>
                 | <foreach_stmt>
                 | <when_stmt>

<repeat_stmt> ::= "repeat" <number> "times" "{" <statement_list> "}"

<foreach_stmt> ::= "foreach" <identifier> "in" <identifier> "{" <statement_list> "}"

<when_stmt> ::= "when" <condition> "then" "{" <statement_list> "}"
              | "when" <condition> "then" "{" <statement_list> "}" 
                "else" "{" <statement_list> "}"

<condition> ::= <expression> <comparison_op> <expression>

<comparison_op> ::= "==" | "!=" | ">" | "<" | ">=" | "<="

<expression> ::= <term>
               | <expression> "+" <term>
               | <expression> "-" <term>

<term> ::= <factor>
         | <term> "*" <factor>
         | <term> "/" <factor>

<factor> ::= <number>
           | <identifier>
           | "(" <expression> ")"

<number> ::= [0-9]+ | [0-9]+ "." [0-9]+

<identifier> ::= [a-zA-Z_][a-zA-Z0-9_]*

<text_literal> ::= '"' [characters]* '"'

<comment> ::= "#" [characters until newline]
```

## 4. Semantic Rules

### 4.1 Type System

**Primitive Types:**
- `ingredient` - Food ingredients with quantities
- `time` - Duration values (minutes, seconds, hours)
- `temp` - Temperature values (F, C)
- `quantity` - Numeric amounts with units
- `text` - String values

### 4.2 Type Compatibility

**Allowed Operations:**
- `ingredient` can be mixed, added, scaled
- `time` can be added, subtracted
- `temp` can be compared
- `quantity` supports arithmetic operations

### 4.3 Scope Rules

- Global scope for all declarations
- Block scope for control structures
- Variables must be declared before use

### 4.4 Semantic Checks

1. Ingredient must be declared before mixing
2. Temperature must be valid (0-500 F or 0-260 C)
3. Time must be positive
4. Quantity must be positive
5. Type compatibility in operations

## 5. Example Programs

### Example 1: Scalable Recipe with Input
```recipe
# Dynamic recipe that scales based on servings
input servings;

ingredient flour = 0.5 * servings cups;
ingredient sugar = 0.25 * servings cups;
temp oven = 350 F;

heat oven to 350 F;
mix flour with sugar;
wait 15 minutes;
serve "Cookies ready!";
```

### Example 2: Simple Cookie Recipe
```recipe
ingredient flour = 2 cups;
ingredient sugar = 1 cup;
ingredient butter = 0.5 cups;
temp oven = 350 F;

heat oven to 350 F;
mix flour with sugar with butter;
wait 15 minutes;
serve "Cookies ready!";
```

### Example 2: Scaled Recipe
```recipe
ingredient rice = 1 cups;
quantity servings = 4;

scale rice by 2;
wait 20 minutes;
serve "Rice for 8 people";
```

### Example 3: Conditional Cooking
```recipe
temp current = 300 F;
temp target = 350 F;

when current < target then {
    heat oven to 350 F;
    wait 10 minutes;
}
serve "Oven ready";
```

### Example 4: Repeated Steps
```recipe
ingredient dough = 1 lbs;

repeat 3 times {
    mix dough;
    wait 5 minutes;
}
serve "Dough kneaded";
```

## 6. Compiler Phases

### Phase 1: Lexical Analysis
- Tokenize recipe instructions
- Recognize keywords, units, identifiers
- Handle comments

### Phase 2: Syntax Analysis
- Build parse tree
- Validate grammar rules
- Create AST

### Phase 3: Semantic Analysis
- Type checking
- Symbol table construction
- Validate ingredient usage

### Phase 4: Intermediate Code Generation
- Generate three-address code
- Translate operations to TAC

### Phase 5: Optimization
- Constant folding
- Dead code elimination
- Instruction reordering

### Phase 6: Code Generation
- Generate executable instructions
- Produce recipe execution plan

## 7. Error Handling

### Lexical Errors
- Invalid character
- Unterminated string
- Invalid number format

### Syntax Errors
- Missing semicolon
- Unexpected token
- Unmatched braces

### Semantic Errors
- Undeclared ingredient
- Type mismatch
- Invalid temperature range
- Negative time/quantity

### Runtime Errors
- Division by zero
- Invalid operation
- Missing ingredient

## 8. File Extension
- `.recipe` - RecipeScript source files

## 9. Future Enhancements
1. Recipe functions/procedures
2. Ingredient substitution rules
3. Nutritional calculation
4. Multi-recipe meal planning
5. Shopping list generation
6. Timing optimization
7. Recipe import/export
8. Unit conversion automation
