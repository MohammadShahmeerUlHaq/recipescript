# CHART PAPER 7: COMPLETE COMPILATION PROCESS
## RecipeScript - End-to-End Example

---

## COMPLETE EXAMPLE

**Source Code:**
```recipe
ingredient flour = 2 cups;
ingredient sugar = 1 cups;
mix flour with sugar;
```

---

## PHASE 1: LEXICAL ANALYSIS

### Input: Character Stream
```
i n g r e d i e n t   f l o u r   =   2   c u p s ; ...
```

### Output: Token Stream
```
┌────────┬──────────────┬────────┬────────┐
│ Token  │ Lexeme       │ Type   │ Line   │
├────────┼──────────────┼────────┼────────┤
│ KEYWORD│ ingredient   │ TYPE   │ 1      │
│ ID     │ flour        │ ID     │ 1      │
│ ASSIGN │ =            │ OP     │ 1      │
│ NUMBER │ 2            │ NUM    │ 1      │
│ UNIT   │ cups         │ UNIT   │ 1      │
│ SEMI   │ ;            │ DELIM  │ 1      │
│ KEYWORD│ ingredient   │ TYPE   │ 2      │
│ ID     │ sugar        │ ID     │ 2      │
│ ASSIGN │ =            │ OP     │ 2      │
│ NUMBER │ 1            │ NUM    │ 2      │
│ UNIT   │ cups         │ UNIT   │ 2      │
│ SEMI   │ ;            │ DELIM  │ 2      │
│ KEYWORD│ mix          │ OP     │ 3      │
│ ID     │ flour        │ ID     │ 3      │
│ KEYWORD│ with         │ PREP   │ 3      │
│ ID     │ sugar        │ ID     │ 3      │
│ SEMI   │ ;            │ DELIM  │ 3      │
│ EOF    │              │ EOF    │ 3      │
└────────┴──────────────┴────────┴────────┘
```

---

## PHASE 2: SYNTAX ANALYSIS

### Input: Token Stream

### Output: Parse Tree
```
                        <program>
                            |
                     <statement_list>
                    /       |        \
                   /        |         \
            <statement> <statement> <statement>
                |           |           |
          <declaration> <declaration> <operation>
           /    |    \    /    |    \      |
          /     |     \  /     |     \     |
      <type>  <id>  <value> <type> <id> <value>  <mix>
         |      |    /  \     |     |    /  \      |
    ingredient flour /   \  ingredient sugar /  \ <ing_list>
                   /     \              /    \   /    \
               <expr>  <unit>       <expr> <unit> flour with sugar
                  |       |            |      |
               <term>   cups        <term>  cups
                  |                    |
              <factor>             <factor>
                  |                    |
                  2                    1
```

### Abstract Syntax Tree (AST) - Simplified:
```
Program
├── Declaration(ingredient, flour, 2, cups)
├── Declaration(ingredient, sugar, 1, cups)
└── Operation(mix, [flour, sugar])
```

---

## PHASE 3: SEMANTIC ANALYSIS

### Symbol Table Construction:
```
┌──────────┬──────────┬──────────┬──────────┬──────────┐
│ Name     │ Type     │ Value    │ Unit     │ Line     │
├──────────┼──────────┼──────────┼──────────┼──────────┤
│ flour    │ingredient│ 2.0      │ cups     │ 1        │
│ sugar    │ingredient│ 1.0      │ cups     │ 2        │
└──────────┴──────────┴──────────┴──────────┴──────────┘
```

### Semantic Checks:
```
✓ Line 1: flour declared as ingredient
✓ Line 2: sugar declared as ingredient
✓ Line 3: flour exists in symbol table
✓ Line 3: sugar exists in symbol table
✓ Line 3: flour is ingredient type (valid for mix)
✓ Line 3: sugar is ingredient type (valid for mix)
✓ All checks passed!
```

### Type Checking:
```
mix operation requires: ingredient types
flour: ingredient ✓
sugar: ingredient ✓
Result: Type check passed
```

---

## PHASE 4: INTERMEDIATE CODE GENERATION

### Three Address Code (TAC):
```
# Line 1: ingredient flour = 2 cups;
t1 = 2
t2 = "cups"
flour = t1
flour.unit = t2
flour.type = "ingredient"

# Line 2: ingredient sugar = 1 cups;
t3 = 1
t4 = "cups"
sugar = t3
sugar.unit = t4
sugar.type = "ingredient"

# Line 3: mix flour with sugar;
t5 = flour
t6 = sugar
t7 = mix(t5, t6)
```

### Control Flow Graph:
```
┌─────────────────────┐
│ Entry               │
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│ t1 = 2              │
│ flour = t1          │
│ flour.unit = "cups" │
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│ t3 = 1              │
│ sugar = t3          │
│ sugar.unit = "cups" │
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│ t5 = flour          │
│ t6 = sugar          │
│ t7 = mix(t5, t6)    │
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│ Exit                │
└─────────────────────┘
```

---

## PHASE 5: CODE OPTIMIZATION

### Before Optimization:
```
t1 = 2
t2 = "cups"
flour = t1
flour.unit = t2
flour.type = "ingredient"
t3 = 1
t4 = "cups"
sugar = t3
sugar.unit = t4
sugar.type = "ingredient"
t5 = flour
t6 = sugar
t7 = mix(t5, t6)
```

### After Optimization:
```
# Constant folding
flour = 2
flour.unit = "cups"
flour.type = "ingredient"

sugar = 1
sugar.unit = "cups"
sugar.type = "ingredient"

# Copy propagation
t7 = mix(flour, sugar)
```

### Optimizations Applied:
1. **Constant Folding:** t1=2, flour=t1 → flour=2
2. **Copy Propagation:** t5=flour, mix(t5) → mix(flour)
3. **Dead Code Elimination:** Removed unused t1, t2, t3, t4, t5, t6

---

## PHASE 6: CODE GENERATION

### Target Code (Python-like):
```python
# Initialize ingredients
flour = {
    'value': 2.0,
    'unit': 'cups',
    'type': 'ingredient'
}

sugar = {
    'value': 1.0,
    'unit': 'cups',
    'type': 'ingredient'
}

# Execute mix operation
print(f"Mixing {flour['value']} {flour['unit']} of flour")
print(f"with {sugar['value']} {sugar['unit']} of sugar")
```

### Execution Output:
```
Mixing 2.0 cups of flour
with 1.0 cups of sugar
```

---

## COMPLETE COMPILATION PIPELINE

```
┌─────────────────────────────────────────────────────────┐
│                    SOURCE CODE                          │
│         ingredient flour = 2 cups;                      │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              LEXICAL ANALYZER (Scanner)                 │
│  - Tokenization                                         │
│  - Remove whitespace/comments                           │
│  - Identify keywords, identifiers, literals             │
└────────────────────┬────────────────────────────────────┘
                     │ Token Stream
                     ▼
┌─────────────────────────────────────────────────────────┐
│              SYNTAX ANALYZER (Parser)                   │
│  - Build parse tree                                     │
│  - Check grammar rules                                  │
│  - Create AST                                           │
└────────────────────┬────────────────────────────────────┘
                     │ Parse Tree / AST
                     ▼
┌─────────────────────────────────────────────────────────┐
│              SEMANTIC ANALYZER                          │
│  - Type checking                                        │
│  - Symbol table construction                            │
│  - Scope resolution                                     │
│  - Semantic validation                                  │
└────────────────────┬────────────────────────────────────┘
                     │ Annotated AST + Symbol Table
                     ▼
┌─────────────────────────────────────────────────────────┐
│         INTERMEDIATE CODE GENERATOR                     │
│  - Generate TAC                                         │
│  - Create CFG                                           │
│  - Temporary variable allocation                        │
└────────────────────┬────────────────────────────────────┘
                     │ Three Address Code
                     ▼
┌─────────────────────────────────────────────────────────┐
│              CODE OPTIMIZER                             │
│  - Constant folding                                     │
│  - Copy propagation                                     │
│  - Dead code elimination                                │
│  - Common subexpression elimination                     │
└────────────────────┬────────────────────────────────────┘
                     │ Optimized TAC
                     ▼
┌─────────────────────────────────────────────────────────┐
│              CODE GENERATOR                             │
│  - Target code generation                               │
│  - Register allocation                                  │
│  - Instruction selection                                │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                  TARGET CODE                            │
│              (Executable Program)                       │
└─────────────────────────────────────────────────────────┘
```

---

## COMPLEX EXAMPLE WITH ALL PHASES

**Source Code:**
```recipe
input servings;
ingredient flour = 0.5 * servings cups;
when flour > 2 then {
    serve "Large batch";
} else {
    serve "Small batch";
}
```

### PHASE 1: Tokens
```
input, servings, ;, ingredient, flour, =, 0.5, *, servings, 
cups, ;, when, flour, >, 2, then, {, serve, "Large batch", 
;, }, else, {, serve, "Small batch", ;, }
```

### PHASE 2: AST
```
Program
├── Input(servings)
├── Declaration(ingredient, flour, 0.5 * servings, cups)
└── When
    ├── Condition(flour > 2)
    ├── Then: Serve("Large batch")
    └── Else: Serve("Small batch")
```

### PHASE 3: Symbol Table
```
┌──────────┬──────────┬──────────┬──────────┐
│ Name     │ Type     │ Value    │ Unit     │
├──────────┼──────────┼──────────┼──────────┤
│ servings │ quantity │ input    │ -        │
│ flour    │ingredient│ computed │ cups     │
└──────────┴──────────┴──────────┴──────────┘
```

### PHASE 4: TAC
```
servings = input()
t1 = 0.5
t2 = servings
t3 = t1 * t2
flour = t3
flour.unit = "cups"
t4 = flour
t5 = 2
t6 = t4 > t5
if_false t6 goto L1
t7 = "Large batch"
serve(t7)
goto L2
L1:
t8 = "Small batch"
serve(t8)
L2:
```

### PHASE 5: Optimized TAC
```
servings = input()
t1 = 0.5 * servings
flour = t1
flour.unit = "cups"
if_false (flour > 2) goto L1
serve("Large batch")
goto L2
L1:
serve("Small batch")
L2:
```

### PHASE 6: Target Code
```python
servings = int(input("Enter servings: "))
flour = 0.5 * servings

if flour > 2:
    print("Large batch")
else:
    print("Small batch")
```

---

## ERROR HANDLING ACROSS PHASES

### Lexical Errors:
```
Source: ingredient fl@ur = 2 cups;
Error: Invalid character '@' at line 1, column 14
```

### Syntax Errors:
```
Source: ingredient flour = 2 cups
Error: Missing semicolon at line 1
```

### Semantic Errors:
```
Source: mix flour with sugar;
Error: Undeclared variable 'flour' at line 1
```

### Type Errors:
```
Source: temp oven = 350 F;
        mix oven;
Error: Type mismatch - 'mix' requires ingredient, got temp
```

---

## COMPILER DATA STRUCTURES

### 1. Token
```
struct Token {
    type: TokenType
    lexeme: string
    value: any
    line: int
    column: int
}
```

### 2. AST Node
```
struct ASTNode {
    type: NodeType
    children: List<ASTNode>
    value: any
    line: int
}
```

### 3. Symbol Table Entry
```
struct SymbolEntry {
    name: string
    type: string
    value: any
    unit: string
    scope: string
    line: int
}
```

### 4. TAC Instruction
```
struct TACInstruction {
    op: string
    arg1: string
    arg2: string
    result: string
}
```

---

## COMPILATION TIME COMPLEXITY

```
┌──────────────────────┬─────────────────┐
│ Phase                │ Complexity      │
├──────────────────────┼─────────────────┤
│ Lexical Analysis     │ O(n)            │
│ Syntax Analysis      │ O(n)            │
│ Semantic Analysis    │ O(n)            │
│ IR Generation        │ O(n)            │
│ Optimization         │ O(n²) - O(n³)   │
│ Code Generation      │ O(n)            │
├──────────────────────┼─────────────────┤
│ Total (worst case)   │ O(n³)           │
└──────────────────────┴─────────────────┘

n = number of source code tokens/statements
```

---

## MEMORY USAGE

```
┌──────────────────────┬─────────────────┐
│ Data Structure       │ Space           │
├──────────────────────┼─────────────────┤
│ Token List           │ O(n)            │
│ Parse Tree           │ O(n)            │
│ Symbol Table         │ O(v)            │
│ Recipe Table         │ O(r)            │
│ TAC Instructions     │ O(n)            │
│ CFG                  │ O(n)            │
├──────────────────────┼─────────────────┤
│ Total                │ O(n + v + r)    │
└──────────────────────┴─────────────────┘

n = tokens, v = variables, r = recipes
```

---

## RECIPE FUNCTION EXAMPLE

**Source Code:**
```recipe
recipe double_quantity(quantity x) returns quantity {
    quantity result = x * 2;
    return result;
}

quantity servings = 4;
quantity doubled = double_quantity(servings);
display doubled;
```

### PHASE 1: Tokens
```
recipe, double_quantity, (, quantity, x, ), returns, quantity, {,
quantity, result, =, x, *, 2, ;, return, result, ;, },
quantity, servings, =, 4, ;,
quantity, doubled, =, double_quantity, (, servings, ), ;,
display, doubled, ;
```

### PHASE 2: AST
```
Program
├── Recipes
│   └── RecipeDeclaration(double_quantity)
│       ├── Params: [(quantity, x)]
│       ├── Returns: quantity
│       └── Body:
│           ├── Declaration(quantity, result, x * 2)
│           └── Return(result)
└── Statements
    ├── Declaration(quantity, servings, 4)
    ├── Declaration(quantity, doubled, double_quantity(servings))
    └── Display(doubled)
```

### PHASE 3: Symbol Table
```
RECIPE TABLE:
┌──────────────────┬──────────────┬──────────────┐
│ double_quantity  │ (quantity x) │ quantity     │
└──────────────────┴──────────────┴──────────────┘

VARIABLE TABLE:
┌──────────┬──────────┬──────────┐
│ servings │ quantity │ 4        │
│ doubled  │ quantity │ computed │
└──────────┴──────────┴──────────┘
```

### PHASE 4: TAC
```
RECIPE double_quantity:
    t0 = x * 2
    result = t0
    RETURN result
END_RECIPE double_quantity

servings = 4
PARAM servings
t1 = CALL double_quantity, 1
doubled = t1
display doubled
```

### PHASE 5: Optimized TAC
```
RECIPE double_quantity:
    result = x * 2
    RETURN result
END_RECIPE double_quantity

servings = 4
PARAM servings
doubled = CALL double_quantity, 1
display doubled
```

### PHASE 6: Execution Output
```
doubled: 8
```

---
