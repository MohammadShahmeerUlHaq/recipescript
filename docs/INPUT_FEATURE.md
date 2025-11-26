# Input Parameters Feature - RecipeScript

## Overview

RecipeScript now supports **input parameters** that allow recipes to be dynamic and scalable based on user input. This makes recipes more flexible and practical for real-world use.

## Syntax

```recipe
input variable_name;
```

The `input` statement declares a variable that will be provided by the user at runtime.

## Usage

### Basic Example

```recipe
# Ask user for number of servings
input servings;

# Calculate ingredients based on servings
ingredient flour = 0.5 * servings cups;
ingredient sugar = 0.25 * servings cups;

serve "Recipe for servings people!";
```

### How It Works

1. **Declaration**: `input servings;` declares an input variable
2. **User Prompt**: At runtime, user is prompted: "Enter value for servings:"
3. **Calculation**: Arithmetic expressions use the input value
4. **Dynamic Scaling**: All ingredients scale automatically

## Arithmetic in Declarations

You can now use arithmetic expressions in ingredient declarations:

```recipe
ingredient flour = 0.5 * servings cups;
ingredient sugar = 100 + 50 * people grams;
ingredient water = (base + extra) * 2 ml;
```

**Supported Operators:**
- `*` Multiplication
- `/` Division
- `+` Addition
- `-` Subtraction

## Complete Example

```recipe
# Scalable Cookie Recipe
input servings;

# 0.5 cups flour per serving
ingredient flour = 0.5 * servings cups;
ingredient sugar = 0.25 * servings cups;
ingredient butter = 0.125 * servings cups;

temp oven = 350 F;

heat oven to 350 F;
mix flour with sugar with butter;
wait 15 minutes;

serve "Cookies ready!";
```

**Running:**
```bash
python recipescript.py recipe.recipe
Enter value for servings: 8
```

**Result:**
- flour = 4 cups (0.5 * 8)
- sugar = 2 cups (0.25 * 8)
- butter = 1 cups (0.125 * 8)

## Interactive vs Non-Interactive Mode

### Interactive Mode
When running normally, the user is prompted for input:
```bash
python recipescript.py recipe.recipe
Enter value for servings: 4
```

### Non-Interactive Mode (Testing)
In automated testing or piped input, defaults to 4:
```bash
echo "" | python recipescript.py recipe.recipe
# Uses default value of 4
```

## Test Files

- **tests/test7_input_auto.recipe** - Automated test with input
- **examples/scalable_pasta.recipe** - Full example with input

## Benefits

1. **Flexibility**: One recipe works for any number of servings
2. **Practicality**: Real-world recipes need to scale
3. **Reusability**: Same recipe file for different quantities
4. **Calculations**: Automatic ingredient scaling

## Technical Details

### Token Type
- New token: `INPUT`
- Keyword: `input`

### AST Node
- `InputStatement(var_name)`

### Symbol Table
- Input variables declared as `QUANTITY` type

### TAC Generation
- Generates: `input variable_name`

### Execution
- Prompts user for input
- Stores value in variable
- Used in arithmetic expressions

## Examples

### Example 1: Simple Scaling
```recipe
input people;
ingredient pasta = 100 * people grams;
serve "Pasta for people people!";
```

### Example 2: Multiple Inputs
```recipe
input servings;
input spice_level;

ingredient flour = 2 * servings cups;
ingredient chili = 1 * spice_level tsp;
```

### Example 3: Complex Calculations
```recipe
input guests;
input extra_hungry;

# Base + extra for hungry guests
ingredient rice = (100 * guests) + (50 * extra_hungry) grams;
```

## Limitations

- Input variables are always numeric (quantity type)
- Cannot input strings or other types
- One input per statement
- Input must be declared before use

## Future Enhancements

Potential improvements:
- String input support
- Default values: `input servings default 4;`
- Input validation: `input servings range 1 to 20;`
- Multiple inputs in one statement
- Input from file or command-line arguments

---

**This feature makes RecipeScript more practical and demonstrates advanced compiler concepts!**
