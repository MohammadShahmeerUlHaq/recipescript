# CHART PAPER 6: INTERMEDIATE CODE GENERATION
## RecipeScript - Three Address Code (TAC)

---

## INTERMEDIATE REPRESENTATION OVERVIEW

**Purpose:** Bridge between high-level source and low-level machine code

**Benefits:**
1. Machine-independent optimization
2. Easier code generation for multiple targets
3. Simplifies compiler structure
4. Enables better optimization

---

## THREE ADDRESS CODE (TAC)

**Format:** `result = operand1 operator operand2`

**Characteristics:**
- At most 3 addresses per instruction
- One operator per instruction
- Temporary variables for intermediate results

---

## TAC INSTRUCTION TYPES

### 1. Assignment
```
x = y
x = 5
```

### 2. Binary Operations
```
x = y + z
x = y - z
x = y * z
x = y / z
```

### 3. Unary Operations
```
x = -y
x = !y
```

### 4. Copy
```
x = y
```

### 5. Conditional Jump
```
if x < y goto L1
if x == y goto L1
if x != y goto L1
```

### 6. Unconditional Jump
```
goto L1
```

### 7. Labels
```
L1:
```

### 8. Function Calls
```
param x
call func, n
x = call func, n
```

### 9. Return
```
return x
return
```

### 10. Recipe Declaration
```
RECIPE recipe_name:
...
END_RECIPE recipe_name
```

### 11. Recipe Call
```
PARAM arg1
PARAM arg2
result = CALL recipe_name, arg_count
```

---

## EXAMPLE 1: SIMPLE DECLARATION

**Source Code:**
```recipe
ingredient flour = 2 cups;
```

**Three Address Code:**
```
t1 = 2
t2 = "cups"
flour = t1
flour.unit = t2
flour.type = "ingredient"
```

---

## EXAMPLE 2: ARITHMETIC EXPRESSION

**Source Code:**
```recipe
quantity result = 2 + 3 * 4;
```

**Three Address Code:**
```
t1 = 3
t2 = 4
t3 = t1 * t2        # t3 = 12
t4 = 2
t5 = t4 + t3        # t5 = 14
result = t5
result.type = "quantity"
```

**Parse Tree:**
```
        =
       / \
   result  +
          / \
         2   *
            / \
           3   4
```

**TAC Generation (Post-order traversal):**
```
1. Visit 3 → t1 = 3
2. Visit 4 → t2 = 4
3. Visit * → t3 = t1 * t2
4. Visit 2 → t4 = 2
5. Visit + → t5 = t4 + t3
6. Visit = → result = t5
```

---

## EXAMPLE 3: MIX OPERATION

**Source Code:**
```recipe
mix flour with sugar with butter;
```

**Three Address Code:**
```
t1 = flour
t2 = sugar
t3 = mix(t1, t2)
t4 = butter
t5 = mix(t3, t4)
```

---

## EXAMPLE 4: CONDITIONAL STATEMENT

**Source Code:**
```recipe
temp current = 300 F;
temp target = 350 F;

when current < target then {
    heat oven to 350 F;
}
```

**Three Address Code:**
```
current = 300
current.unit = "F"
target = 350
target.unit = "F"

# Condition evaluation
t1 = current
t2 = target
t3 = t1 < t2
if_false t3 goto L1

# Then block
t4 = 350
t5 = "F"
heat(oven, t4, t5)

L1:
# Continue
```

---

## EXAMPLE 5: REPEAT LOOP

**Source Code:**
```recipe
repeat 3 times {
    mix dough;
    wait 5 minutes;
}
```

**Three Address Code:**
```
# Initialize counter
t1 = 0
t2 = 3

L1:
# Check condition
t3 = t1 < t2
if_false t3 goto L2

# Loop body
mix(dough)
t4 = 5
t5 = "minutes"
wait(t4, t5)

# Increment counter
t1 = t1 + 1
goto L1

L2:
# Continue after loop
```

---

## EXAMPLE 6: WHEN-ELSE STATEMENT

**Source Code:**
```recipe
when flour > 2 then {
    serve "Enough flour";
} else {
    serve "Need more flour";
}
```

**Three Address Code:**
```
# Evaluate condition
t1 = flour
t2 = 2
t3 = t1 > t2
if_false t3 goto L1

# Then block
t4 = "Enough flour"
serve(t4)
goto L2

# Else block
L1:
t5 = "Need more flour"
serve(t5)

L2:
# Continue
```

---

## EXAMPLE 7: COMPLEX EXPRESSION

**Source Code:**
```recipe
quantity result = (2 + 3) * (4 - 1);
```

**Three Address Code:**
```
# Evaluate (2 + 3)
t1 = 2
t2 = 3
t3 = t1 + t2        # t3 = 5

# Evaluate (4 - 1)
t4 = 4
t5 = 1
t6 = t4 - t5        # t6 = 3

# Multiply results
t7 = t3 * t6        # t7 = 15

# Assign to result
result = t7
result.type = "quantity"
```

---

## EXAMPLE 8: INPUT WITH EXPRESSION

**Source Code:**
```recipe
input servings;
ingredient flour = 0.5 * servings cups;
```

**Three Address Code:**
```
# Input
servings = input()

# Calculate flour amount
t1 = 0.5
t2 = servings
t3 = t1 * t2
flour = t3
flour.unit = "cups"
flour.type = "ingredient"
```

---

## EXAMPLE 9: SCALE OPERATION

**Source Code:**
```recipe
ingredient rice = 1 cups;
scale rice by 2;
```

**Three Address Code:**
```
# Declaration
rice = 1
rice.unit = "cups"
rice.type = "ingredient"

# Scale operation
t1 = rice
t2 = 2
t3 = t1 * t2
rice = t3
```

---

## EXAMPLE 10: NESTED CONTROL FLOW

**Source Code:**
```recipe
repeat 2 times {
    when flour > 0 then {
        mix flour;
    }
}
```

**Three Address Code:**
```
# Outer loop initialization
t1 = 0
t2 = 2

L1:
# Outer loop condition
t3 = t1 < t2
if_false t3 goto L4

# Inner condition
t4 = flour
t5 = 0
t6 = t4 > t5
if_false t6 goto L2

# Inner then block
mix(flour)

L2:
# End inner condition

# Increment outer loop
t1 = t1 + 1
goto L1

L4:
# End outer loop
```

---

## EXAMPLE 11: RECIPE FUNCTION DECLARATION

**Source Code:**
```recipe
recipe make_dough(ingredient flour, ingredient water) returns ingredient {
    mix flour with water;
    return flour;
}
```

**Three Address Code:**
```
RECIPE make_dough:
    mix flour, water
    RETURN flour
END_RECIPE make_dough
```

---

## EXAMPLE 12: RECIPE FUNCTION CALL

**Source Code:**
```recipe
ingredient flour = 2 cups;
ingredient water = 1 cups;
ingredient dough = make_dough(flour, water);
```

**Three Address Code:**
```
flour = 2 cups
water = 1 cups

# Push arguments
PARAM flour
PARAM water

# Call recipe
t1 = CALL make_dough, 2

# Store result
dough = t1
```

---

## EXAMPLE 13: RECIPE WITH CALCULATION

**Source Code:**
```recipe
recipe double_quantity(quantity x) returns quantity {
    quantity result = x * 2;
    return result;
}

quantity servings = 4;
quantity doubled = double_quantity(servings);
```

**Three Address Code:**
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
```

---

## TEMPORARY VARIABLE MANAGEMENT

### Naming Convention:
```
t1, t2, t3, ..., tn
```

### Allocation Strategy:
```
1. Generate new temp for each intermediate result
2. Reuse temps after their last use (optimization)
3. Track temp lifetime for register allocation
```

### Example:
```
x = a + b       # t1 = a + b, x = t1
y = c + d       # t2 = c + d, y = t2
z = x + y       # t3 = x + y, z = t3

Can reuse: t1 and t2 after computing z
```

---

## LABEL MANAGEMENT

### Label Generation:
```
L1, L2, L3, ..., Ln
```

### Usage:
- Loop entry points
- Conditional branch targets
- End of blocks

### Example:
```
L1:                 # Loop start
    ...
    goto L1         # Jump back

L2:                 # Loop end
    ...
```

---

## TRANSLATION SCHEMES

### For Assignment:
```
S → id = E
{
    S.code = E.code || 
             gen(id.name '=' E.place)
}
```

### For Binary Operation:
```
E → E1 + E2
{
    E.place = newtemp()
    E.code = E1.code || E2.code ||
             gen(E.place '=' E1.place '+' E2.place)
}
```

### For If-Then:
```
S → if E then S1
{
    L1 = newlabel()
    S.code = E.code ||
             gen('if_false' E.place 'goto' L1) ||
             S1.code ||
             gen(L1 ':')
}
```

### For While Loop:
```
S → while E do S1
{
    L1 = newlabel()
    L2 = newlabel()
    S.code = gen(L1 ':') ||
             E.code ||
             gen('if_false' E.place 'goto' L2) ||
             S1.code ||
             gen('goto' L1) ||
             gen(L2 ':')
}
```

---

## ADDRESSING MODES IN TAC

### 1. Immediate
```
x = 5
```

### 2. Direct
```
x = y
```

### 3. Indexed
```
x = a[i]
a[i] = x
```

### 4. Indirect
```
x = *p
*p = x
```

---

## OPTIMIZATION OPPORTUNITIES

### 1. Constant Folding
```
Before: t1 = 2 + 3
After:  t1 = 5
```

### 2. Constant Propagation
```
Before: x = 5
        y = x + 3
After:  x = 5
        y = 8
```

### 3. Copy Propagation
```
Before: x = y
        z = x + 1
After:  x = y
        z = y + 1
```

### 4. Dead Code Elimination
```
Before: x = 5      # x never used
        y = 10
After:  y = 10
```

### 5. Common Subexpression Elimination
```
Before: t1 = a + b
        t2 = a + b
        x = t1 * t2
After:  t1 = a + b
        x = t1 * t1
```

---

## CONTROL FLOW GRAPH (CFG)

### Example CFG for If-Then-Else:
```
        ┌─────────────┐
        │   Entry     │
        └──────┬──────┘
               │
        ┌──────▼──────┐
        │  Condition  │
        └──┬───────┬──┘
           │       │
      True │       │ False
           │       │
    ┌──────▼──┐ ┌──▼──────┐
    │  Then   │ │  Else   │
    └──┬──────┘ └──┬──────┘
       │           │
       └─────┬─────┘
             │
        ┌────▼─────┐
        │   Exit   │
        └──────────┘
```

---

## BASIC BLOCKS

**Definition:** Maximal sequence of consecutive instructions with:
1. Single entry point (first instruction)
2. Single exit point (last instruction)
3. No internal branches

### Example:
```
Basic Block 1:
    t1 = 2
    t2 = 3
    t3 = t1 + t2

Basic Block 2:
    if t3 > 5 goto L1

Basic Block 3:
    t4 = t3 * 2
    goto L2

Basic Block 4 (L1):
    t4 = t3 + 1

Basic Block 5 (L2):
    result = t4
```

---

## ADVANTAGES OF TAC

1. ✓ Machine-independent
2. ✓ Easy to optimize
3. ✓ Simple instruction format
4. ✓ Easy to generate code from
5. ✓ Explicit control flow
6. ✓ Explicit temporary variables

---

## DISADVANTAGES OF TAC

1. ✗ More instructions than source
2. ✗ Many temporary variables
3. ✗ Requires additional passes
4. ✗ Memory overhead

---
