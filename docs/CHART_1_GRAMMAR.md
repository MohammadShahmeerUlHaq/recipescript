# CHART PAPER 1: COMPLETE GRAMMAR (BNF)
## RecipeScript Language - Context-Free Grammar

---

## PRODUCTION RULES

### Program Structure
```
<program> ::= <statement_list>

<statement_list> ::= <statement>
                   | <statement> <statement_list>
```

### Statements
```
<statement> ::= <input_stmt> ";"
              | <declaration> ";"
              | <operation> ";"
              | <control_flow>
              | <comment>
```

### Input Statement
```
<input_stmt> ::= "input" <identifier>
```

### Declarations
```
<declaration> ::= <type> <identifier> "=" <value>

<type> ::= "ingredient" 
         | "time" 
         | "temp" 
         | "quantity" 
         | "text"

<value> ::= <expression> <unit>
          | <expression>
          | <text_literal>
          | <identifier>
```

### Units
```
<unit> ::= "cups" | "tbsp" | "tsp" | "grams" | "ml" | "oz" | "lbs"
         | "F" | "C"
         | "minutes" | "seconds" | "hours"
```

### Operations
```
<operation> ::= "mix" <ingredient_list>
              | "heat" <identifier> "to" <value>
              | "wait" <time_value>
              | "serve" <text_literal>
              | "display" <identifier>
              | "add" <identifier> "to" <identifier>
              | "scale" <identifier> "by" <number>

<ingredient_list> ::= <identifier>
                    | <identifier> "with" <ingredient_list>

<time_value> ::= <number> "minutes"
               | <number> "seconds"
               | <number> "hours"
```

### Control Flow
```
<control_flow> ::= <repeat_stmt>
                 | <foreach_stmt>
                 | <when_stmt>

<repeat_stmt> ::= "repeat" <number> "times" "{" <statement_list> "}"

<foreach_stmt> ::= "foreach" <identifier> "in" <identifier> 
                   "{" <statement_list> "}"

<when_stmt> ::= "when" <condition> "then" "{" <statement_list> "}"
              | "when" <condition> "then" "{" <statement_list> "}" 
                "else" "{" <statement_list> "}"
```

### Conditions & Expressions
```
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
```

### Terminals
```
<number> ::= [0-9]+ 
           | [0-9]+ "." [0-9]+

<identifier> ::= [a-zA-Z_][a-zA-Z0-9_]*

<text_literal> ::= '"' [characters]* '"'

<comment> ::= "#" [characters until newline]
```

---

## GRAMMAR CLASSIFICATION

**Type:** Context-Free Grammar (CFG)
**Class:** LL(1) - Suitable for Top-Down Parsing
**Ambiguity:** Unambiguous
**Recursion:** Left-recursion eliminated in expressions

---

## START SYMBOL
```
S = <program>
```

---

## TERMINALS (Σ)
```
Keywords: ingredient, time, temp, quantity, text, mix, heat, 
          wait, serve, display, add, scale, repeat, foreach, 
          when, then, else, times, in, input, to, with, for, 
          at, from, by

Operators: =, +, -, *, /, ==, !=, >, <, >=, <=

Delimiters: ;, ,, (, ), {, }

Units: cups, tbsp, tsp, grams, ml, oz, lbs, F, C, 
       minutes, seconds, hours

Literals: NUMBER, IDENTIFIER, STRING
```

---

## NON-TERMINALS (N)
```
<program>, <statement_list>, <statement>, <input_stmt>,
<declaration>, <type>, <value>, <unit>, <operation>,
<ingredient_list>, <control_flow>, <repeat_stmt>,
<foreach_stmt>, <when_stmt>, <condition>, <comparison_op>,
<expression>, <term>, <factor>, <number>, <identifier>,
<text_literal>, <comment>, <time_value>
```

---

## EXAMPLE DERIVATION

**Input:** `ingredient flour = 2 cups;`

**Derivation:**
```
<program>
=> <statement_list>
=> <statement>
=> <declaration> ";"
=> <type> <identifier> "=" <value> ";"
=> "ingredient" <identifier> "=" <value> ";"
=> "ingredient" "flour" "=" <value> ";"
=> "ingredient" "flour" "=" <expression> <unit> ";"
=> "ingredient" "flour" "=" <term> <unit> ";"
=> "ingredient" "flour" "=" <factor> <unit> ";"
=> "ingredient" "flour" "=" <number> <unit> ";"
=> "ingredient" "flour" "=" "2" <unit> ";"
=> "ingredient" "flour" "=" "2" "cups" ";"
```

---

## GRAMMAR PROPERTIES

1. **Deterministic:** Yes - No ambiguous productions
2. **Left-Recursive:** No - Eliminated in expression rules
3. **Left-Factored:** Yes - Common prefixes factored out
4. **LL(1) Compatible:** Yes - Can use recursive descent
5. **Operator Precedence:** 
   - Highest: *, /
   - Middle: +, -
   - Lowest: Comparison operators
6. **Associativity:** Left-associative for all operators

---
