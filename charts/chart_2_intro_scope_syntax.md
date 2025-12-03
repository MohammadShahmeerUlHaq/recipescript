# RecipeScript

## Introduction

**RecipeScript** is a domain-specific programming language (DSL) designed specifically for writing cooking recipes in a structured, executable format. It combines the clarity of traditional recipe writing with the power of programming constructs like variables, functions, loops, and conditionals.

### Purpose
RecipeScript allows you to:
- Write recipes as executable programs
- Calculate ingredient quantities dynamically based on servings
- Scale recipes automatically
- Reuse recipe components through functions
- Add conditional logic for different cooking scenarios

### Design Philosophy
- **Domain-Specific**: Built specifically for cooking recipes
- **Type-Safe**: Strong typing for ingredients, quantities, temperatures, and time
- **Readable**: Syntax resembles natural recipe language
- **Executable**: Recipes can be compiled and run to generate instructions

---

## Language Scope

### What RecipeScript Can Do
- Declare typed variables (ingredients, quantities, temperatures, time)
- Perform arithmetic calculations for scaling recipes
- Define reusable recipe functions with parameters
- Use conditional logic (when/else)
- Repeat operations with loops
- Mix, heat, wait, scale, and add ingredients
- Display values and serve messages
- Accept user input for dynamic recipes

### What RecipeScript Cannot Do
- File I/O operations
- Network operations
- Complex data structures (arrays, objects)
- String manipulation
- Exception handling

---

## Type System

RecipeScript has 5 built-in types:

| Type | Purpose | Example Values |
|------|---------|----------------|
| `ingredient` | Food items with quantities | `flour = 500 grams` |
| `quantity` | Numeric values | `servings = 4` |
| `temp` | Temperatures | `oven = 350 F` |
| `time` | Durations | `baking_time = 30 minutes` |
| `text` | String values | `message = "Hello"` |

---

## Sample Syntax

### Variable Declaration

```recipe
type name = value unit;
```

### Arithmetic Operations

```recipe
type name = operand1 operator operand2;
```

### Input Statement

```recipe
input people;   # Prompts: "Enter value for people:"
```

### Display Operations

```recipe
display flour;  # Output: flour: 500 grams
serve "Recipe complete!";   # Output: Recipe complete!
```

### Conditional Statements

```recipe
when conidtion then {
    body
} else {
    body
}
```

### Loops

```recipe
repeat n times {
    body
}
```

### Function Declaration

```recipe
recipe name(parameters) returns type {
    body
}
```

### Function Calls

```recipe
ingredient dough = make_dough(flour, water);
```

---

### Operations

```recipe
# Mix ingredients together
mix flour with water;
mix flour with water with yeast;
mix dough;

# Heat something to a temperature
heat oven to 350 F;
heat pan to 200 C;

# Wait for a duration
wait 5 minutes;

# Scale an ingredient by a factor
scale flour by 1.5;

# Add one ingredient to another
add salt to flour;
```

### Comments

```recipe
# This is a single-line comment
```
---

## Error Messages

**Undeclared Variable:**
```
Semantic Error: Variable 'flour' not declared
```

**Type Mismatch:**
```
Semantic Error: Cannot mix non-ingredient: servings
```

**Division by Zero:**
```
Runtime Error: Division by zero
```

**Missing Return:**
```
Semantic Error: Recipe 'make_dough' must return a value
```
---