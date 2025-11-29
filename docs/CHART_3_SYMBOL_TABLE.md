# CHART PAPER 3: SYMBOL TABLE MANAGEMENT
## RecipeScript - Symbol Table Structure & Scope Management

---

## SYMBOL TABLE STRUCTURE

### Variable Entry Format
```
┌──────────────┬──────────┬──────────┬──────────┬──────────┬──────────┐
│ Name         │ Type     │ Value    │ Unit     │ Scope    │ Line No  │
├──────────────┼──────────┼──────────┼──────────┼──────────┼──────────┤
│ flour        │ingredient│ 2.0      │ cups     │ global   │ 1        │
│ sugar        │ingredient│ 1.0      │ cups     │ global   │ 2        │
│ oven         │ temp     │ 350      │ F        │ global   │ 3        │
│ servings     │ quantity │ 4        │ -        │ global   │ 4        │
│ i            │ quantity │ 0        │ -        │ block_1  │ 10       │
└──────────────┴──────────┴──────────┴──────────┴──────────┴──────────┘
```

### Recipe Entry Format
```
┌──────────────┬──────────────────────┬──────────────┬──────────┐
│ Name         │ Parameters           │ Return Type  │ Line No  │
├──────────────┼──────────────────────┼──────────────┼──────────┤
│ make_dough   │ (ingredient, ingr.)  │ ingredient   │ 1        │
│ double_qty   │ (quantity)           │ quantity     │ 5        │
│ bake_pizza   │ (ingr., ingr., temp) │ -            │ 10       │
└──────────────┴──────────────────────┴──────────────┴──────────┘
```

### Attributes Stored

**For Variables:**
1. **Name** - Identifier string
2. **Type** - ingredient, time, temp, quantity, text
3. **Value** - Current value (if known at compile time)
4. **Unit** - cups, grams, F, minutes, etc.
5. **Scope** - global, block_1, block_2, recipe_1, etc.
6. **Line Number** - Declaration location
7. **Is Initialized** - Boolean flag
8. **Is Used** - Boolean flag (for optimization)

**For Recipes:**
1. **Name** - Recipe identifier
2. **Parameters** - List of (type, name) pairs
3. **Return Type** - Return type or None
4. **Line Number** - Declaration location
5. **Body** - AST of recipe body

---

## SCOPE MANAGEMENT

### Scope Hierarchy
```
┌─────────────────────────────────────────┐
│         GLOBAL SCOPE (Level 0)          │
│  - All top-level declarations           │
│  - Accessible everywhere                │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │   BLOCK SCOPE 1 (Level 1)         │ │
│  │   - repeat/foreach/when blocks    │ │
│  │   - Local variables               │ │
│  │                                   │ │
│  │  ┌─────────────────────────────┐ │ │
│  │  │ BLOCK SCOPE 2 (Level 2)     │ │ │
│  │  │ - Nested blocks             │ │ │
│  │  │ - Inner local variables     │ │ │
│  │  └─────────────────────────────┘ │ │
│  └───────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

### Scope Stack
```
Top → [Block_2] → [Block_1] → [Global] ← Bottom
```

**Lookup Algorithm:**
1. Search current scope (top of stack)
2. If not found, search parent scope
3. Continue until found or reach global scope
4. If not found in global → ERROR: Undeclared variable

---

## EXAMPLE 1: SIMPLE RECIPE

### Source Code:
```recipe
ingredient flour = 2 cups;
ingredient sugar = 1 cups;
temp oven = 350 F;

mix flour with sugar;
heat oven to 350 F;
```

### Symbol Table:
```
┌──────────┬──────────┬──────────┬──────────┬──────────┬──────────┐
│ Name     │ Type     │ Value    │ Unit     │ Scope    │ Line     │
├──────────┼──────────┼──────────┼──────────┼──────────┼──────────┤
│ flour    │ingredient│ 2.0      │ cups     │ global   │ 1        │
│ sugar    │ingredient│ 1.0      │ cups     │ global   │ 2        │
│ oven     │ temp     │ 350      │ F        │ global   │ 3        │
└──────────┴──────────┴──────────┴──────────┴──────────┴──────────┘
```

---

## EXAMPLE 2: WITH CONTROL FLOW

### Source Code:
```recipe
ingredient dough = 1 lbs;
quantity count = 3;

repeat 3 times {
    quantity i = 0;
    mix dough;
}
```

### Symbol Table with Scopes:
```
GLOBAL SCOPE:
┌──────────┬──────────┬──────────┬──────────┬──────────┬──────────┐
│ Name     │ Type     │ Value    │ Unit     │ Scope    │ Line     │
├──────────┼──────────┼──────────┼──────────┼──────────┼──────────┤
│ dough    │ingredient│ 1.0      │ lbs      │ global   │ 1        │
│ count    │ quantity │ 3        │ -        │ global   │ 2        │
└──────────┴──────────┴──────────┴──────────┴──────────┴──────────┘

BLOCK SCOPE (repeat):
┌──────────┬──────────┬──────────┬──────────┬──────────┬──────────┐
│ Name     │ Type     │ Value    │ Unit     │ Scope    │ Line     │
├──────────┼──────────┼──────────┼──────────┼──────────┼──────────┤
│ i        │ quantity │ 0        │ -        │ block_1  │ 4        │
└──────────┴──────────┴──────────┴──────────┴──────────┴──────────┘
```

---

## EXAMPLE 3: NESTED SCOPES

### Source Code:
```recipe
ingredient flour = 2 cups;

when flour > 1 then {
    quantity extra = 0.5;
    
    repeat 2 times {
        quantity temp = extra * 2;
        display temp;
    }
}
```

### Symbol Table Structure:
```
GLOBAL SCOPE (Level 0):
┌──────────┬──────────┬──────────┬──────────┬──────────┐
│ flour    │ingredient│ 2.0      │ cups     │ Line 1   │
└──────────┴──────────┴──────────┴──────────┴──────────┘

WHEN BLOCK (Level 1):
┌──────────┬──────────┬──────────┬──────────┬──────────┐
│ extra    │ quantity │ 0.5      │ -        │ Line 4   │
└──────────┴──────────┴──────────┴──────────┴──────────┘

REPEAT BLOCK (Level 2):
┌──────────┬──────────┬──────────┬──────────┬──────────┐
│ temp     │ quantity │ 1.0      │ -        │ Line 7   │
└──────────┴──────────┴──────────┴──────────┴──────────┘
```

**Variable Access:**
- `temp` can access: temp (local), extra (parent), flour (global)
- `extra` can access: extra (local), flour (global)
- `flour` can access: flour (local/global only)

---

## EXAMPLE 4: RECIPE FUNCTIONS

### Source Code:
```recipe
recipe make_dough(ingredient flour, ingredient water) returns ingredient {
    mix flour with water;
    return flour;
}

ingredient flour = 2 cups;
ingredient water = 1 cups;
ingredient dough = make_dough(flour, water);
```

### Symbol Table Structure:
```
RECIPE TABLE:
┌──────────────┬──────────────────────┬──────────────┬──────────┐
│ make_dough   │ (ingredient flour,   │ ingredient   │ Line 1   │
│              │  ingredient water)   │              │          │
└──────────────┴──────────────────────┴──────────────┴──────────┘

GLOBAL SCOPE (Level 0):
┌──────────┬──────────┬──────────┬──────────┬──────────┐
│ flour    │ingredient│ 2.0      │ cups     │ Line 6   │
│ water    │ingredient│ 1.0      │ cups     │ Line 7   │
│ dough    │ingredient│ result   │ -        │ Line 8   │
└──────────┴──────────┴──────────┴──────────┴──────────┘

RECIPE SCOPE (make_dough):
┌──────────┬──────────┬──────────┬──────────┬──────────┐
│ flour    │ingredient│ param    │ -        │ Line 1   │
│ water    │ingredient│ param    │ -        │ Line 1   │
└──────────┴──────────┴──────────┴──────────┴──────────┘
```

**Scope Rules for Recipes:**
- Recipe parameters are in recipe scope
- Recipe body can access parameters and global variables
- Recipe calls pass arguments by value
- Return statement exits recipe and returns value

---

## SYMBOL TABLE OPERATIONS

### 1. INSERT
```
insert(name, type, value, unit, scope, line):
    if name exists in current_scope:
        ERROR: "Variable already declared"
    else:
        add entry to symbol_table[current_scope]
```

### 2. LOOKUP
```
lookup(name):
    scope = current_scope
    while scope != null:
        if name in symbol_table[scope]:
            return symbol_table[scope][name]
        scope = parent_scope(scope)
    ERROR: "Undeclared variable"
```

### 3. UPDATE
```
update(name, value):
    entry = lookup(name)
    if entry:
        entry.value = value
        entry.is_initialized = true
    else:
        ERROR: "Variable not found"
```

### 4. ENTER_SCOPE
```
enter_scope():
    scope_level++
    create new scope: "block_" + scope_level
    push scope onto scope_stack
```

### 5. EXIT_SCOPE
```
exit_scope():
    pop scope from scope_stack
    remove all entries in popped scope
    scope_level--
```

---

## TYPE CHECKING WITH SYMBOL TABLE

### Type Compatibility Matrix
```
┌────────────┬──────┬──────┬──────┬──────┬──────┐
│ Operation  │ ingr │ time │ temp │ qty  │ text │
├────────────┼──────┼──────┼──────┼──────┼──────┤
│ mix        │  ✓   │  ✗   │  ✗   │  ✗   │  ✗   │
│ heat       │  ✗   │  ✗   │  ✓   │  ✗   │  ✗   │
│ wait       │  ✗   │  ✓   │  ✗   │  ✗   │  ✗   │
│ serve      │  ✗   │  ✗   │  ✗   │  ✗   │  ✓   │
│ add        │  ✓   │  ✗   │  ✗   │  ✗   │  ✗   │
│ scale      │  ✓   │  ✗   │  ✗   │  ✓   │  ✗   │
│ arithmetic │  ✗   │  ✓   │  ✓   │  ✓   │  ✗   │
│ comparison │  ✗   │  ✓   │  ✓   │  ✓   │  ✗   │
└────────────┴──────┴──────┴──────┴──────┴──────┘
```

### Type Checking Algorithm
```
check_operation(operation, operands):
    for each operand in operands:
        entry = lookup(operand)
        if entry.type not compatible with operation:
            ERROR: "Type mismatch"
        if not entry.is_initialized:
            WARNING: "Using uninitialized variable"
```

---

## SEMANTIC CHECKS USING SYMBOL TABLE

### 1. Declaration Check
```
Before use: Check if variable exists in symbol table
If not found: ERROR "Undeclared variable 'name'"
```

### 2. Type Check
```
For each operation: Verify operand types match requirements
If mismatch: ERROR "Type error: expected X, got Y"
```

### 3. Initialization Check
```
Before use: Check is_initialized flag
If false: WARNING "Variable may be uninitialized"
```

### 4. Scope Check
```
Variable access: Verify variable is accessible in current scope
If not: ERROR "Variable 'name' not in scope"
```

### 5. Redeclaration Check
```
On declaration: Check if name exists in current scope
If exists: ERROR "Variable 'name' already declared"
```

---

## IMPLEMENTATION DATA STRUCTURE

### Hash Table (Dictionary)
```python
symbol_table = {
    'global': {
        'flour': {
            'type': 'ingredient',
            'value': 2.0,
            'unit': 'cups',
            'line': 1,
            'initialized': True,
            'used': True
        },
        'sugar': {...}
    },
    'block_1': {
        'i': {...}
    }
}

scope_stack = ['global', 'block_1']
current_scope = 'block_1'
```

---

## SYMBOL TABLE LIFECYCLE

```
1. INITIALIZATION
   - Create global scope
   - Initialize scope stack

2. DECLARATION PHASE
   - Parse declarations
   - Insert into symbol table
   - Check for redeclarations

3. USAGE PHASE
   - Lookup variables on use
   - Verify types
   - Mark as used

4. SCOPE MANAGEMENT
   - Enter scope on block start
   - Exit scope on block end
   - Clean up local variables

5. OPTIMIZATION PHASE
   - Remove unused variables
   - Constant propagation
   - Dead code elimination
```

---
