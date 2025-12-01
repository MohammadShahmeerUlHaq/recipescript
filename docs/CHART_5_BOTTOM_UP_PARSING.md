# CHART PAPER 5: BOTTOM-UP PARSING
## RecipeScript - LR Parsing (Shift-Reduce)

---

## BOTTOM-UP PARSING OVERVIEW

**Definition:** Parse tree construction from leaves to root (bottom to top)

**Method:** LR Parsing (Shift-Reduce)
- **L** = Left-to-right scan
- **R** = Rightmost derivation in reverse
- Uses a **stack** and **parsing table**

**Note:** Bottom-up parsing can handle left-recursive grammars directly, unlike top-down parsing. The examples below use simplified grammar rules for clarity. The actual RecipeScript grammar is LL(1) compatible (see CHART_1 and CHART_4).

---

## SHIFT-REDUCE PARSING ACTIONS

### Four Possible Actions:

1. **SHIFT** - Push next input token onto stack
2. **REDUCE** - Replace handle on stack with non-terminal
3. **ACCEPT** - Parsing completed successfully
4. **ERROR** - Syntax error detected

---

## PARSING EXAMPLE 1

**Input:** `ingredient flour = 2 cups;`

**Grammar Rules:**
```
1. <program> → <statement>
2. <statement> → <declaration> ;
3. <declaration> → <type> <id> = <value>
4. <type> → ingredient
5. <value> → <number> <unit>
6. <number> → 2
7. <unit> → cups
```

**Parsing Steps:**

```
┌──────┬─────────────────────────────┬──────────────────────┬──────────┐
│ Step │ Stack                       │ Input                │ Action   │
├──────┼─────────────────────────────┼──────────────────────┼──────────┤
│  1   │ $                           │ ingredient flour = 2 │ SHIFT    │
│      │                             │ cups ;$              │          │
├──────┼─────────────────────────────┼──────────────────────┼──────────┤
│  2   │ $ ingredient                │ flour = 2 cups ;$    │ REDUCE 4 │
│      │                             │                      │ (type)   │
├──────┼─────────────────────────────┼──────────────────────┼──────────┤
│  3   │ $ <type>                    │ flour = 2 cups ;$    │ SHIFT    │
├──────┼─────────────────────────────┼──────────────────────┼──────────┤
│  4   │ $ <type> flour              │ = 2 cups ;$          │ SHIFT    │
├──────┼─────────────────────────────┼──────────────────────┼──────────┤
│  5   │ $ <type> flour =            │ 2 cups ;$            │ SHIFT    │
├──────┼─────────────────────────────┼──────────────────────┼──────────┤
│  6   │ $ <type> flour = 2          │ cups ;$              │ REDUCE 6 │
│      │                             │                      │ (number) │
├──────┼─────────────────────────────┼──────────────────────┼──────────┤
│  7   │ $ <type> flour = <number>   │ cups ;$              │ SHIFT    │
├──────┼─────────────────────────────┼──────────────────────┼──────────┤
│  8   │ $ <type> flour = <number>   │ ;$                   │ REDUCE 7 │
│      │ cups                        │                      │ (unit)   │
├──────┼─────────────────────────────┼──────────────────────┼──────────┤
│  9   │ $ <type> flour = <number>   │ ;$                   │ REDUCE 5 │
│      │ <unit>                      │                      │ (value)  │
├──────┼─────────────────────────────┼──────────────────────┼──────────┤
│ 10   │ $ <type> flour = <value>    │ ;$                   │ REDUCE 3 │
│      │                             │                      │ (decl)   │
├──────┼─────────────────────────────┼──────────────────────┼──────────┤
│ 11   │ $ <declaration>             │ ;$                   │ SHIFT    │
├──────┼─────────────────────────────┼──────────────────────┼──────────┤
│ 12   │ $ <declaration> ;           │ $                    │ REDUCE 2 │
│      │                             │                      │ (stmt)   │
├──────┼─────────────────────────────┼──────────────────────┼──────────┤
│ 13   │ $ <statement>               │ $                    │ REDUCE 1 │
│      │                             │                      │ (program)│
├──────┼─────────────────────────────┼──────────────────────┼──────────┤
│ 14   │ $ <program>                 │ $                    │ ACCEPT   │
└──────┴─────────────────────────────┴──────────────────────┴──────────┘
```

---

## PARSING EXAMPLE 2

**Input:** `mix flour with sugar;`

**Grammar Rules:**
```
1. <statement> → <operation> ;
2. <operation> → mix <ing_list>
3. <ing_list> → <id> with <ing_list>
4. <ing_list> → <id>
5. <id> → flour
6. <id> → sugar
```

**Parsing Steps:**

```
┌──────┬─────────────────────────────┬──────────────────────┬──────────┐
│ Step │ Stack                       │ Input                │ Action   │
├──────┼─────────────────────────────┼──────────────────────┼──────────┤
│  1   │ $                           │ mix flour with       │ SHIFT    │
│      │                             │ sugar ;$             │          │
├──────┼─────────────────────────────┼──────────────────────┼──────────┤
│  2   │ $ mix                       │ flour with sugar ;$  │ SHIFT    │
├──────┼─────────────────────────────┼──────────────────────┼──────────┤
│  3   │ $ mix flour                 │ with sugar ;$        │ REDUCE 5 │
│      │                             │                      │ (id)     │
├──────┼─────────────────────────────┼──────────────────────┼──────────┤
│  4   │ $ mix <id>                  │ with sugar ;$        │ SHIFT    │
├──────┼─────────────────────────────┼──────────────────────┼──────────┤
│  5   │ $ mix <id> with             │ sugar ;$             │ SHIFT    │
├──────┼─────────────────────────────┼──────────────────────┼──────────┤
│  6   │ $ mix <id> with sugar       │ ;$                   │ REDUCE 6 │
│      │                             │                      │ (id)     │
├──────┼─────────────────────────────┼──────────────────────┼──────────┤
│  7   │ $ mix <id> with <id>        │ ;$                   │ REDUCE 4 │
│      │                             │                      │(ing_list)│
├──────┼─────────────────────────────┼──────────────────────┼──────────┤
│  8   │ $ mix <id> with <ing_list>  │ ;$                   │ REDUCE 3 │
│      │                             │                      │(ing_list)│
├──────┼─────────────────────────────┼──────────────────────┼──────────┤
│  9   │ $ mix <ing_list>            │ ;$                   │ REDUCE 2 │
│      │                             │                      │ (oper)   │
├──────┼─────────────────────────────┼──────────────────────┼──────────┤
│ 10   │ $ <operation>               │ ;$                   │ SHIFT    │
├──────┼─────────────────────────────┼──────────────────────┼──────────┤
│ 11   │ $ <operation> ;             │ $                    │ REDUCE 1 │
│      │                             │                      │ (stmt)   │
├──────┼─────────────────────────────┼──────────────────────┼──────────┤
│ 12   │ $ <statement>               │ $                    │ ACCEPT   │
└──────┴─────────────────────────────┴──────────────────────┴──────────┘
```

---

## PARSING EXAMPLE 3 (Expressions)

**Input:** `2 + 3 * 4`

**Grammar Rules:**
```
1. <expr> → <expr> + <term>
2. <expr> → <term>
3. <term> → <term> * <factor>
4. <term> → <factor>
5. <factor> → <number>
6. <number> → 2 | 3 | 4
```

**Parsing Steps:**

```
┌──────┬─────────────────────────────┬──────────────────────┬──────────┐
│ Step │ Stack                       │ Input                │ Action   │
├──────┼─────────────────────────────┼──────────────────────┼──────────┤
│  1   │ $                           │ 2 + 3 * 4 $          │ SHIFT    │
├──────┼─────────────────────────────┼──────────────────────┼──────────┤
│  2   │ $ 2                         │ + 3 * 4 $            │ REDUCE 6 │
├──────┼─────────────────────────────┼──────────────────────┼──────────┤
│  3   │ $ <number>                  │ + 3 * 4 $            │ REDUCE 5 │
├──────┼─────────────────────────────┼──────────────────────┼──────────┤
│  4   │ $ <factor>                  │ + 3 * 4 $            │ REDUCE 4 │
├──────┼─────────────────────────────┼──────────────────────┼──────────┤
│  5   │ $ <term>                    │ + 3 * 4 $            │ REDUCE 2 │
├──────┼─────────────────────────────┼──────────────────────┼──────────┤
│  6   │ $ <expr>                    │ + 3 * 4 $            │ SHIFT    │
├──────┼─────────────────────────────┼──────────────────────┼──────────┤
│  7   │ $ <expr> +                  │ 3 * 4 $              │ SHIFT    │
├──────┼─────────────────────────────┼──────────────────────┼──────────┤
│  8   │ $ <expr> + 3                │ * 4 $                │ REDUCE 6 │
├──────┼─────────────────────────────┼──────────────────────┼──────────┤
│  9   │ $ <expr> + <number>         │ * 4 $                │ REDUCE 5 │
├──────┼─────────────────────────────┼──────────────────────┼──────────┤
│ 10   │ $ <expr> + <factor>         │ * 4 $                │ REDUCE 4 │
├──────┼─────────────────────────────┼──────────────────────┼──────────┤
│ 11   │ $ <expr> + <term>           │ * 4 $                │ SHIFT    │
├──────┼─────────────────────────────┼──────────────────────┼──────────┤
│ 12   │ $ <expr> + <term> *         │ 4 $                  │ SHIFT    │
├──────┼─────────────────────────────┼──────────────────────┼──────────┤
│ 13   │ $ <expr> + <term> * 4       │ $                    │ REDUCE 6 │
├──────┼─────────────────────────────┼──────────────────────┼──────────┤
│ 14   │ $ <expr> + <term> * <number>│ $                    │ REDUCE 5 │
├──────┼─────────────────────────────┼──────────────────────┼──────────┤
│ 15   │ $ <expr> + <term> * <factor>│ $                    │ REDUCE 3 │
├──────┼─────────────────────────────┼──────────────────────┼──────────┤
│ 16   │ $ <expr> + <term>           │ $                    │ REDUCE 1 │
├──────┼─────────────────────────────┼──────────────────────┼──────────┤
│ 17   │ $ <expr>                    │ $                    │ ACCEPT   │
└──────┴─────────────────────────────┴──────────────────────┴──────────┘

Result: 2 + (3 * 4) = 14  [Correct precedence maintained!]
```

---

## LR(0) ITEMS

**Item:** Production with a dot (•) showing parsing progress

**Example Items for:** `<declaration> → <type> <id> = <value>`

```
<declaration> → • <type> <id> = <value>    [Initial]
<declaration> → <type> • <id> = <value>    [After type]
<declaration> → <type> <id> • = <value>    [After id]
<declaration> → <type> <id> = • <value>    [After =]
<declaration> → <type> <id> = <value> •    [Complete]
```

---

## LR(0) AUTOMATON (Partial)

### State 0 (Initial):
```
<program> → • <statement>
<statement> → • <declaration> ;
<statement> → • <operation> ;
<declaration> → • <type> <id> = <value>
<type> → • ingredient
<type> → • time
```

### State 1 (After 'ingredient'):
```
<type> → ingredient •
```

### State 2 (After <type>):
```
<declaration> → <type> • <id> = <value>
<id> → • IDENTIFIER
```

### State 3 (After <type> <id>):
```
<declaration> → <type> <id> • = <value>
```

### State 4 (After <type> <id> =):
```
<declaration> → <type> <id> = • <value>
<value> → • <expr> <unit>
<expr> → • <term>
<term> → • <factor>
<factor> → • NUMBER
```

---

## SLR PARSING TABLE (Simplified)

```
┌───────┬─────────────────────────────┬─────────────────────────────┐
│ State │ ACTION                      │ GOTO                        │
│       ├──────┬──────┬──────┬────────┼──────┬──────┬──────┬───────┤
│       │ ingr │  id  │  =   │   ;    │ prog │ stmt │ decl │ type  │
├───────┼──────┼──────┼──────┼────────┼──────┼──────┼──────┼───────┤
│   0   │  s1  │      │      │        │      │  g2  │  g3  │  g4   │
│   1   │  r4  │      │      │        │      │      │      │       │
│   2   │      │      │      │ accept │      │      │      │       │
│   3   │      │      │      │   s5   │      │      │      │       │
│   4   │      │  s6  │      │        │      │      │      │       │
│   5   │  r2  │      │      │        │      │      │      │       │
│   6   │      │      │  s7  │        │      │      │      │       │
│   7   │      │      │      │        │      │      │      │       │
└───────┴──────┴──────┴──────┴────────┴──────┴──────┴──────┴───────┘

Legend:
s = shift (and go to state)
r = reduce (by production number)
g = goto (state)
```

---

## HANDLE IDENTIFICATION

**Handle:** Substring matching right side of production, ready to reduce

**Example:** `ingredient flour = 2 cups`

```
Stack: $ ingredient
Handle: "ingredient" matches <type> → ingredient
Action: REDUCE to <type>

Stack: $ <type> flour = 2
Handle: "2" matches <number> → 2
Action: REDUCE to <number>

Stack: $ <type> flour = <number> cups
Handle: "<number> cups" matches <value> → <number> <unit>
Action: REDUCE to <value>
```

---

## RIGHTMOST DERIVATION (Reverse)

**Input:** `ingredient flour = 2 cups;`

**Rightmost Derivation (Forward):**
```
<program>
⇒ <statement>
⇒ <declaration> ;
⇒ <type> <id> = <value> ;
⇒ ingredient <id> = <value> ;
⇒ ingredient flour = <value> ;
⇒ ingredient flour = <number> <unit> ;
⇒ ingredient flour = 2 <unit> ;
⇒ ingredient flour = 2 cups ;
```

**Bottom-Up Parsing (Reverse Rightmost):**
```
ingredient flour = 2 cups ;
⇐ ingredient flour = <number> cups ;
⇐ ingredient flour = <number> <unit> ;
⇐ ingredient flour = <value> ;
⇐ ingredient <id> = <value> ;
⇐ <type> <id> = <value> ;
⇐ <declaration> ;
⇐ <statement>
⇐ <program>
```

---

## ADVANTAGES OF BOTTOM-UP PARSING

1. ✓ More powerful than top-down (handles more grammars)
2. ✓ Can handle left recursion naturally
3. ✓ Efficient (linear time with table)
4. ✓ Detects errors early
5. ✓ Suitable for automatic parser generators (yacc, bison)

---

## DISADVANTAGES

1. ✗ More complex to implement by hand
2. ✗ Harder to understand
3. ✗ Less intuitive error messages
4. ✗ Requires parsing table construction

---

## PARSING EXAMPLE 4 (Recipe Function Call)

**Input:** `ingredient dough = make_dough(flour, water);`

**Grammar Rules:**
```
1. <statement> → <declaration> ;
2. <declaration> → <type> <id> = <value>
3. <type> → ingredient
4. <value> → <recipe_call>
5. <recipe_call> → <id> ( <arg_list> )
6. <arg_list> → <id> , <id>
```

**Parsing Steps:**

```
┌──────┬─────────────────────────────┬──────────────────────┬──────────┐
│ Step │ Stack                       │ Input                │ Action   │
├──────┼─────────────────────────────┼──────────────────────┼──────────┤
│  1   │ $                           │ ingredient dough = ..│ SHIFT    │
├──────┼─────────────────────────────┼──────────────────────┼──────────┤
│  2   │ $ ingredient                │ dough = make_dough...│ REDUCE 3 │
├──────┼─────────────────────────────┼──────────────────────┼──────────┤
│  3   │ $ <type>                    │ dough = make_dough...│ SHIFT    │
├──────┼─────────────────────────────┼──────────────────────┼──────────┤
│  4   │ $ <type> dough              │ = make_dough(...)    │ SHIFT    │
├──────┼─────────────────────────────┼──────────────────────┼──────────┤
│  5   │ $ <type> dough =            │ make_dough(...)      │ SHIFT    │
├──────┼─────────────────────────────┼──────────────────────┼──────────┤
│  6   │ $ <type> dough = make_dough │ (flour, water);      │ SHIFT    │
├──────┼─────────────────────────────┼──────────────────────┼──────────┤
│  7   │ $ <type> dough = make_dough(│ flour, water);       │ SHIFT    │
├──────┼─────────────────────────────┼──────────────────────┼──────────┤
│  8   │ $ ... make_dough( flour     │ , water);            │ SHIFT    │
├──────┼─────────────────────────────┼──────────────────────┼──────────┤
│  9   │ $ ... make_dough( flour ,   │ water);              │ SHIFT    │
├──────┼─────────────────────────────┼──────────────────────┼──────────┤
│ 10   │ $ ... make_dough( flour,water│ );                  │ REDUCE 6 │
├──────┼─────────────────────────────┼──────────────────────┼──────────┤
│ 11   │ $ ... make_dough( <arg_list>│ );                   │ SHIFT    │
├──────┼─────────────────────────────┼──────────────────────┼──────────┤
│ 12   │ $ ... make_dough(<arg_list>)│ ;                    │ REDUCE 5 │
├──────┼─────────────────────────────┼──────────────────────┼──────────┤
│ 13   │ $ <type> dough = <recipe_call│ ;                   │ REDUCE 4 │
├──────┼─────────────────────────────┼──────────────────────┼──────────┤
│ 14   │ $ <type> dough = <value>    │ ;                    │ REDUCE 2 │
├──────┼─────────────────────────────┼──────────────────────┼──────────┤
│ 15   │ $ <declaration>             │ ;                    │ SHIFT    │
├──────┼─────────────────────────────┼──────────────────────┼──────────┤
│ 16   │ $ <declaration> ;           │ $                    │ REDUCE 1 │
├──────┼─────────────────────────────┼──────────────────────┼──────────┤
│ 17   │ $ <statement>               │ $                    │ ACCEPT   │
└──────┴─────────────────────────────┴──────────────────────┴──────────┘
```

---

## COMPARISON: TOP-DOWN vs BOTTOM-UP

```
┌─────────────────────┬──────────────┬──────────────┐
│ Feature             │ Top-Down     │ Bottom-Up    │
├─────────────────────┼──────────────┼──────────────┤
│ Parse Tree          │ Root → Leaf  │ Leaf → Root  │
│ Derivation          │ Leftmost     │ Rightmost    │
│ Implementation      │ Easy         │ Complex      │
│ Left Recursion      │ No           │ Yes          │
│ Grammar Class       │ LL(k)        │ LR(k)        │
│ Power               │ Less         │ More         │
│ Error Messages      │ Better       │ Harder       │
│ Manual Coding       │ Preferred    │ Difficult    │
│ Parser Generators   │ ANTLR        │ Yacc, Bison  │
│ Recipe Functions    │ Supported    │ Supported    │
└─────────────────────┴──────────────┴──────────────┘
```

---

## TYPES OF LR PARSERS

### 1. LR(0)
- Simplest
- Limited power
- No lookahead

### 2. SLR (Simple LR)
- Uses FOLLOW sets
- More powerful than LR(0)
- Still limited

### 3. LALR (Look-Ahead LR)
- Most commonly used
- Good balance of power and table size
- Used by yacc, bison

### 4. CLR (Canonical LR)
- Most powerful
- Largest tables
- Rarely used in practice

---

## CONFLICT RESOLUTION

### Shift-Reduce Conflict
```
Stack: $ <expr> +
Input: * ...

Should we:
- SHIFT * (continue building expression)
- REDUCE <expr> (complete current expression)

Resolution: Use precedence rules
```

### Reduce-Reduce Conflict
```
Two different productions can reduce same handle

Resolution: 
- Grammar redesign
- Precedence declarations
```

---
