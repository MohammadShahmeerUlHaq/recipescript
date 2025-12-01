# CHART PAPER 1: COMPLETE GRAMMAR (BNF)
## RecipeScript Language - Context-Free Grammar

---

## PRODUCTION RULES

**Note:** This is an LL(1) grammar with left recursion eliminated.

### Program Structure
```
<program> ::= <recipe_list> <statement_list>
            | <recipe_list>
            | <statement_list>

<recipe_list> ::= <recipe_decl> <recipe_list>
                | <recipe_decl>

<statement_list> ::= <statement> <statement_list>
                   | <statement>
```

### Recipe Functions
```
<recipe_decl> ::= "recipe" IDENTIFIER "(" <param_list> ")" "{" <statement_list> "}"
                | "recipe" IDENTIFIER "(" <param_list> ")" "returns" <type> 
                  "{" <statement_list> "}"

<param_list> ::= <parameter> <param_list'>
               | ε

<param_list'> ::= "," <parameter> <param_list'>
                | ε

<parameter> ::= <type> IDENTIFIER

<recipe_call> ::= IDENTIFIER "(" <arg_list> ")"

<arg_list> ::= <expression> <arg_list'>
             | ε

<arg_list'> ::= "," <expression> <arg_list'>
              | ε
```

### Statements
```
<statement> ::= <input_stmt> ";"
              | <declaration> ";"
              | <operation> ";"
              | <control_flow>
              | <recipe_call> ";"
              | <return_stmt> ";"

<return_stmt> ::= "return" <expression>
                | "return"
```

### Input Statement
```
<input_stmt> ::= "input" IDENTIFIER
```

### Declarations
```
<declaration> ::= <type> IDENTIFIER "=" <value>

<type> ::= "ingredient" 
         | "time" 
         | "temp" 
         | "quantity" 
         | "text"

<value> ::= <expression> <value_tail>
          | STRING

<value_tail> ::= <unit>
               | ε
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
              | "heat" IDENTIFIER "to" <value>
              | "wait" <value>
              | "serve" STRING
              | "display" IDENTIFIER
              | "add" IDENTIFIER "to" IDENTIFIER
              | "scale" IDENTIFIER "by" NUMBER

<ingredient_list> ::= IDENTIFIER <ingredient_list'>

<ingredient_list'> ::= "with" IDENTIFIER <ingredient_list'>
                     | ε
```

### Control Flow
```
<control_flow> ::= <repeat_stmt>
                 | <foreach_stmt>
                 | <when_stmt>

<repeat_stmt> ::= "repeat" NUMBER "times" "{" <statement_list> "}"

<foreach_stmt> ::= "foreach" IDENTIFIER "in" IDENTIFIER 
                   "{" <statement_list> "}"

<when_stmt> ::= "when" <condition> "then" "{" <statement_list> "}" <when_tail>

<when_tail> ::= "else" "{" <statement_list> "}"
              | ε
```

### Conditions & Expressions (Left Recursion Eliminated)
```
<condition> ::= <expression> <comparison_op> <expression>

<comparison_op> ::= "==" | "!=" | ">" | "<" | ">=" | "<="

<expression> ::= <term> <expression'>

<expression'> ::= "+" <term> <expression'>
                | "-" <term> <expression'>
                | ε

<term> ::= <factor> <term'>

<term'> ::= "*" <factor> <term'>
          | "/" <factor> <term'>
          | ε

<factor> ::= NUMBER
           | IDENTIFIER
           | "(" <expression> ")"
           | <recipe_call>
```

### Terminal Symbols (Lexer Tokens)
```
NUMBER      ::= [0-9]+ | [0-9]+\.[0-9]+
IDENTIFIER  ::= [a-zA-Z_][a-zA-Z0-9_]*
STRING      ::= '"' [^"]* '"'
```

### Lexical Notes
- **Comments:** `# ...` handled by lexer, ignored by parser
- **Whitespace:** Ignored by lexer
- **Keywords:** Recognized by lexer as special tokens

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
          at, from, by, recipe, return, returns

Operators: =, +, -, *, /, ==, !=, >, <, >=, <=

Delimiters: ;, ,, (, ), {, }

Units: cups, tbsp, tsp, grams, ml, oz, lbs, F, C, 
       minutes, seconds, hours

Literals: NUMBER, IDENTIFIER, STRING
```

---

## NON-TERMINALS (N)
```
<program>, <recipe_list>, <recipe_decl>, <param_list>, <parameter>,
<statement_list>, <statement>, <input_stmt>, <declaration>, <type>, 
<value>, <unit>, <operation>, <ingredient_list>, <control_flow>, 
<repeat_stmt>, <foreach_stmt>, <when_stmt>, <condition>, 
<comparison_op>, <expression>, <term>, <factor>, <number>, 
<identifier>, <text_literal>, <comment>, <time_value>, 
<recipe_call>, <arg_list>, <return_stmt>
```

---

## EXAMPLE DERIVATION 1

**Input:** `ingredient flour = 2 cups;`

**Derivation:**
```
<program>
=> <recipe_list> <statement_list>
=> ε <statement_list>
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

## EXAMPLE DERIVATION 2 (Recipe Function)

**Input:** `recipe make_dough(ingredient flour) { return flour; }`

**Derivation:**
```
<program>
=> <recipe_list> <statement_list>
=> <recipe_decl> <statement_list>
=> "recipe" <identifier> "(" <param_list> ")" "{" <statement_list> "}" <statement_list>
=> "recipe" "make_dough" "(" <param_list> ")" "{" <statement_list> "}" ε
=> "recipe" "make_dough" "(" <parameter> ")" "{" <statement_list> "}"
=> "recipe" "make_dough" "(" <type> <identifier> ")" "{" <statement_list> "}"
=> "recipe" "make_dough" "(" "ingredient" "flour" ")" "{" <statement_list> "}"
=> "recipe" "make_dough" "(" "ingredient" "flour" ")" "{" <statement> "}"
=> "recipe" "make_dough" "(" "ingredient" "flour" ")" "{" <return_stmt> ";" "}"
=> "recipe" "make_dough" "(" "ingredient" "flour" ")" "{" "return" <expression> ";" "}"
=> "recipe" "make_dough" "(" "ingredient" "flour" ")" "{" "return" "flour" ";" "}"
```

---

## GRAMMAR PROPERTIES

1. **Deterministic:** Yes - No ambiguous productions
2. **Left-Recursive:** No - Eliminated using <expr'> and <term'> productions
3. **Left-Factored:** Yes - Common prefixes factored out (e.g., <value_tail>, <when_tail>)
4. **LL(1) Compatible:** Yes - Can use recursive descent parsing
5. **Operator Precedence:** 
   - Highest: *, / (in <term>)
   - Middle: +, - (in <expression>)
   - Lowest: Comparison operators (in <condition>)
6. **Associativity:** Left-associative for all operators (achieved through tail recursion)

## LEFT RECURSION ELIMINATION

**Original (Left Recursive):**
```
<expression> ::= <expression> "+" <term>
               | <expression> "-" <term>
               | <term>
```

**Transformed (LL(1) Compatible):**
```
<expression> ::= <term> <expression'>
<expression'> ::= "+" <term> <expression'>
                | "-" <term> <expression'>
                | ε
```

This transformation:
- Eliminates left recursion
- Maintains left associativity
- Makes grammar LL(1) parseable

---
