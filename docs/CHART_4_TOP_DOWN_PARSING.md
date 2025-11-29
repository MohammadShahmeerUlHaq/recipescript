# CHART PAPER 4: TOP-DOWN PARSING
## RecipeScript - LL(1) Recursive Descent Parser

---

## TOP-DOWN PARSING OVERVIEW

**Definition:** Parse tree construction from root to leaves (top to bottom)

**Method Used:** Recursive Descent Parsing (LL(1))
- **L** = Left-to-right scan
- **L** = Leftmost derivation
- **(1)** = One lookahead token

---

## FIRST AND FOLLOW SETS

### FIRST Sets
```
FIRST(<program>) = {recipe, input, ingredient, time, temp, quantity, 
                    text, mix, heat, wait, serve, display, 
                    add, scale, repeat, foreach, when, #, ε}

FIRST(<recipe_list>) = {recipe, ε}

FIRST(<recipe_decl>) = {recipe}

FIRST(<statement>) = {input, ingredient, time, temp, quantity, 
                      text, mix, heat, wait, serve, display, 
                      add, scale, repeat, foreach, when, return,
                      IDENTIFIER, #}

FIRST(<declaration>) = {ingredient, time, temp, quantity, text}

FIRST(<operation>) = {mix, heat, wait, serve, display, add, scale}

FIRST(<control_flow>) = {repeat, foreach, when}

FIRST(<recipe_call>) = {IDENTIFIER}

FIRST(<return_stmt>) = {return}

FIRST(<expression>) = {NUMBER, IDENTIFIER, (}

FIRST(<term>) = {NUMBER, IDENTIFIER, (}

FIRST(<factor>) = {NUMBER, IDENTIFIER, (}
```

### FOLLOW Sets
```
FOLLOW(<program>) = {$}

FOLLOW(<statement>) = {input, ingredient, time, temp, quantity, 
                       text, mix, heat, wait, serve, display, 
                       add, scale, repeat, foreach, when, #, }, $}

FOLLOW(<declaration>) = {;}

FOLLOW(<expression>) = {;, ), cups, tbsp, grams, F, C, 
                        minutes, ==, !=, <, >, <=, >=}

FOLLOW(<term>) = {+, -, ;, ), cups, tbsp, grams, F, C, 
                  minutes, ==, !=, <, >, <=, >=}

FOLLOW(<factor>) = {*, /, +, -, ;, ), cups, tbsp, grams, F, C, 
                    minutes, ==, !=, <, >, <=, >=}
```

---

## PREDICTIVE PARSING TABLE (Partial)

```
┌─────────────┬──────────┬──────────┬──────────┬──────────┬──────────┐
│ Non-Term    │ input    │ingredient│   mix    │  repeat  │   when   │
├─────────────┼──────────┼──────────┼──────────┼──────────┼──────────┤
│ <program>   │    1     │    1     │    1     │    1     │    1     │
│ <statement> │    2     │    3     │    4     │    5     │    5     │
│ <input_stmt>│    6     │    -     │    -     │    -     │    -     │
│<declaration>│    -     │    7     │    -     │    -     │    -     │
│ <operation> │    -     │    -     │    8     │    -     │    -     │
│<control_flow│    -     │    -     │    -     │    9     │   10     │
└─────────────┴──────────┴──────────┴──────────┴──────────┴──────────┘

Production Rules:
1: <program> → <statement_list>
2: <statement> → <input_stmt> ;
3: <statement> → <declaration> ;
4: <statement> → <operation> ;
5: <statement> → <control_flow>
6: <input_stmt> → input <identifier>
7: <declaration> → <type> <identifier> = <value>
8: <operation> → mix <ingredient_list>
9: <control_flow> → <repeat_stmt>
10: <control_flow> → <when_stmt>
```

---

## RECURSIVE DESCENT PARSER PSEUDOCODE

### Main Parser Function
```
parse_program():
    recipes = []
    statements = []
    
    # Parse recipe declarations first
    while current_token == 'recipe':
        recipe = parse_recipe_declaration()
        recipes.append(recipe)
    
    # Parse main statements
    while current_token != EOF:
        stmt = parse_statement()
        statements.append(stmt)
    
    return Program(recipes, statements)

parse_recipe_declaration():
    match('recipe')
    name = match(IDENTIFIER)
    match('(')
    params = parse_parameter_list()
    match(')')
    
    return_type = None
    if current_token == 'returns':
        match('returns')
        return_type = match_type()
    
    match('{')
    body = parse_statement_list_until('}')
    match('}')
    
    return RecipeDeclaration(name, params, return_type, body)

parse_parameter_list():
    params = []
    if current_token == ')':
        return params  # Empty list
    
    while True:
        param_type = match_type()
        param_name = match(IDENTIFIER)
        params.append((param_type, param_name))
        
        if current_token != ',':
            break
        match(',')
    
    return params

parse_statement_list():
    statements = []
    while current_token != EOF and current_token != '}':
        stmt = parse_statement()
        statements.append(stmt)
    return statements
```

### Statement Parser
```
parse_statement():
    if current_token == 'input':
        return parse_input_stmt()
    
    elif current_token in ['ingredient', 'time', 'temp', 'quantity', 'text']:
        return parse_declaration()
    
    elif current_token in ['mix', 'heat', 'wait', 'serve', 'display', 
                           'add', 'scale']:
        return parse_operation()
    
    elif current_token in ['repeat', 'foreach', 'when']:
        return parse_control_flow()
    
    elif current_token == '#':
        return parse_comment()
    
    else:
        error("Unexpected token: " + current_token)
```

### Declaration Parser
```
parse_declaration():
    type = match_type()           # ingredient, time, temp, etc.
    name = match(IDENTIFIER)
    match('=')
    value = parse_value()
    match(';')
    
    return DeclarationNode(type, name, value)

parse_value():
    if current_token == STRING:
        return match(STRING)
    else:
        expr = parse_expression()
        if current_token in UNITS:
            unit = match(UNIT)
            return ValueNode(expr, unit)
        return expr
```

### Expression Parser (with precedence)
```
parse_expression():
    # Handles: <expression> → <term> ((+|-) <term>)*
    left = parse_term()
    
    while current_token in ['+', '-']:
        op = current_token
        advance()
        right = parse_term()
        left = BinaryOpNode(op, left, right)
    
    return left

parse_term():
    # Handles: <term> → <factor> ((*|/) <factor>)*
    left = parse_factor()
    
    while current_token in ['*', '/']:
        op = current_token
        advance()
        right = parse_factor()
        left = BinaryOpNode(op, left, right)
    
    return left

parse_factor():
    # Handles: <factor> → NUMBER | IDENTIFIER | ( <expression> )
    if current_token == NUMBER:
        value = current_token.value
        advance()
        return NumberNode(value)
    
    elif current_token == IDENTIFIER:
        name = current_token.value
        advance()
        return IdentifierNode(name)
    
    elif current_token == '(':
        match('(')
        expr = parse_expression()
        match(')')
        return expr
    
    else:
        error("Expected number, identifier, or (")
```

### Operation Parser
```
parse_operation():
    if current_token == 'mix':
        return parse_mix()
    elif current_token == 'heat':
        return parse_heat()
    elif current_token == 'wait':
        return parse_wait()
    elif current_token == 'serve':
        return parse_serve()
    # ... etc

parse_mix():
    match('mix')
    ingredients = parse_ingredient_list()
    match(';')
    return MixNode(ingredients)

parse_ingredient_list():
    # Handles: <ingredient_list> → ID (with ID)*
    ingredients = [match(IDENTIFIER)]
    
    while current_token == 'with':
        match('with')
        ingredients.append(match(IDENTIFIER))
    
    return ingredients
```

### Control Flow Parser
```
parse_control_flow():
    if current_token == 'repeat':
        return parse_repeat()
    elif current_token == 'foreach':
        return parse_foreach()
    elif current_token == 'when':
        return parse_when()

parse_repeat():
    match('repeat')
    count = match(NUMBER)
    match('times')
    match('{')
    body = parse_statement_list_until('}')
    match('}')
    return RepeatNode(count, body)

parse_when():
    match('when')
    condition = parse_condition()
    match('then')
    match('{')
    then_body = parse_statement_list_until('}')
    match('}')
    
    else_body = None
    if current_token == 'else':
        match('else')
        match('{')
        else_body = parse_statement_list_until('}')
        match('}')
    
    return WhenNode(condition, then_body, else_body)

parse_condition():
    left = parse_expression()
    op = match_comparison_op()  # ==, !=, <, >, <=, >=
    right = parse_expression()
    return ConditionNode(op, left, right)
```

### Recipe Call and Return Parser
```
parse_recipe_call():
    # Called when we see IDENTIFIER followed by '('
    name = match(IDENTIFIER)
    match('(')
    args = parse_argument_list()
    match(')')
    return RecipeCallNode(name, args)

parse_argument_list():
    args = []
    if current_token == ')':
        return args  # Empty list
    
    while True:
        arg = parse_expression()
        args.append(arg)
        
        if current_token != ',':
            break
        match(',')
    
    return args

parse_return():
    match('return')
    
    value = None
    if current_token != ';':
        value = parse_expression()
    
    match(';')
    return ReturnNode(value)
```

---

## PARSE TREE EXAMPLE 1

**Input:** `ingredient flour = 2 cups;`

**Parse Tree:**
```
                    <program>
                        |
                 <statement_list>
                        |
                   <statement>
                        |
                 <declaration> ;
                   /    |    \
                  /     |     \
              <type> <id> = <value>
                |     |       /  \
           ingredient flour  /    \
                         <expr>  <unit>
                            |      |
                         <term>  cups
                            |
                        <factor>
                            |
                         <number>
                            |
                            2
```

---

## PARSE TREE EXAMPLE 2

**Input:** `mix flour with sugar;`

**Parse Tree:**
```
                    <program>
                        |
                 <statement_list>
                        |
                   <statement>
                        |
                  <operation> ;
                        |
                    <mix_op>
                    /      \
                  mix   <ingredient_list>
                        /      |      \
                    <id>     with   <ingredient_list>
                      |                  |
                    flour              <id>
                                         |
                                       sugar
```

---

## PARSE TREE EXAMPLE 3

**Input:** `quantity result = 2 + 3 * 4;`

**Parse Tree:**
```
                    <program>
                        |
                   <statement>
                        |
                 <declaration> ;
                   /    |    \
              <type> <id> = <value>
                |     |       |
            quantity result <expr>
                            /  |  \
                        <term> + <term>
                          |        /  |  \
                       <factor> <term> * <factor>
                          |       |         |
                          2    <factor>     4
                                  |
                                  3

Result: 2 + (3 * 4) = 14  [Correct precedence!]
```

---

## PARSE TREE EXAMPLE 4 (Recipe Function)

**Input:** `recipe double(quantity x) returns quantity { return x * 2; }`

**Parse Tree:**
```
                        <program>
                       /        \
                <recipe_list>  <statement_list>
                      |              |
                <recipe_decl>        ε
                /    |    |    \
            recipe  <id> <params> <body>
                     |      |       |
                  double <param> <stmts>
                           |       |
                      (quantity x) <return>
                                    |
                                  return <expr>
                                         /  |  \
                                      <term> * <factor>
                                        |        |
                                     <factor>    2
                                        |
                                        x
```

---

## PARSING ALGORITHM STEPS

### For Input: `ingredient flour = 2 cups;`

```
Step 1: parse_program()
  └─> parse_statement_list()

Step 2: parse_statement()
  └─> current_token = 'ingredient'
  └─> parse_declaration()

Step 3: parse_declaration()
  └─> match('ingredient')  ✓
  └─> match(IDENTIFIER)    ✓ 'flour'
  └─> match('=')           ✓
  └─> parse_value()

Step 4: parse_value()
  └─> parse_expression()
      └─> parse_term()
          └─> parse_factor()
              └─> match(NUMBER) ✓ '2'
  └─> match(UNIT)          ✓ 'cups'

Step 5: match(';')         ✓

Step 6: Return DeclarationNode
```

---

## ERROR RECOVERY STRATEGIES

### 1. Panic Mode
```
On error:
  - Report error
  - Skip tokens until synchronization point
  - Synchronization points: ; } EOF
  - Resume parsing
```

### 2. Phrase Level
```
On error:
  - Insert missing token (e.g., missing semicolon)
  - Delete unexpected token
  - Replace incorrect token
  - Continue parsing
```

### 3. Error Productions
```
Add error productions to grammar:
<statement> → error ;
<expression> → error
```

---

## ADVANTAGES OF TOP-DOWN PARSING

1. ✓ Easy to implement by hand
2. ✓ Easy to understand and debug
3. ✓ Good error messages
4. ✓ Natural for LL(1) grammars
5. ✓ Efficient (linear time)
6. ✓ Predictable behavior

---

## LIMITATIONS

1. ✗ Cannot handle left recursion
2. ✗ Requires left factoring
3. ✗ Limited to LL(k) grammars
4. ✗ May need grammar transformation

---

## LL(1) GRAMMAR REQUIREMENTS

### RecipeScript Grammar is LL(1) because:

1. **No Left Recursion**
   - Original: `<expr> → <expr> + <term>`
   - Transformed: `<expr> → <term> ((+|-) <term>)*`

2. **Left Factored**
   - Common prefixes eliminated
   - Unique first tokens for alternatives

3. **Disjoint FIRST Sets**
   - Each alternative has unique starting token
   - No ambiguity in production choice

4. **Proper FOLLOW Sets**
   - Clear termination points
   - No conflicts

---
