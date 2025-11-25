# RecipeScript - Quick Start Guide

## Get Started in 5 Minutes

### 1. Test the Compiler

Run a simple test:
```bash
python compiler.py test1.recipe
```

You should see all 6 phases execute and output: "Cookies are ready!"

### 2. Run All Tests

```bash
python run_all_tests.py
```

All 6 tests should pass.

### 3. Try Interactive Mode

```bash
python compiler.py
```

Then type:
```recipe
>>> ingredient flour = 2 cups;
>>> serve "Hello RecipeScript!";
>>> exit
```

### 4. Write Your Own Recipe

Create a file `my_recipe.recipe`:
```recipe
# My first recipe
ingredient pasta = 500 grams;
ingredient water = 2 cups;
temp stove = 212 F;

heat stove to 212 F;
mix pasta with water;
wait 10 minutes;
serve "Pasta is ready!";
```

Run it:
```bash
python compiler.py my_recipe.recipe
```

### 5. Language Basics

**Data Types:**
```recipe
ingredient flour = 2 cups;
temp oven = 350 F;
time duration = 30 minutes;
quantity servings = 4;
text message = "Hello";
```

**Operations:**
```recipe
mix flour with sugar;
heat oven to 350 F;
wait 15 minutes;
serve "Done!";
scale flour by 2;
add sugar to flour;
```

**Control Flow:**
```recipe
# Repeat
repeat 3 times {
    mix dough;
}

# Conditional
when temp > 300 then {
    serve "Hot!";
} else {
    serve "Cold!";
}
```

**Units:**
- Volume: cups, tbsp, tsp, ml, oz
- Weight: grams, lbs
- Temperature: F (Fahrenheit), C (Celsius)
- Time: minutes, seconds, hours

### 6. Example Recipes

See test files for examples:
- `test1.recipe` - Simple cookie recipe
- `test2.recipe` - Scaling ingredients
- `test3.recipe` - Conditional cooking
- `test4.recipe` - Repeated steps
- `test5.recipe` - Complex operations
- `test6.recipe` - Different units

### 7. Documentation

- **README.md** - Main documentation
- **LANGUAGE_SPEC.md** - Complete language reference
- **PROJECT_DOCUMENTATION.md** - Technical details
- **HANDWRITTEN_GUIDE.md** - Handwritten artifacts guide
- **reflection.md** - Project reflection

### 8. Common Commands

```bash
# Run a recipe file
python compiler.py recipe.recipe

# Interactive mode
python compiler.py

# Run all tests
python run_all_tests.py

# Test lexer only
python lexer.py
```

### 9. Troubleshooting

**Error: "File not found"**
- Make sure you're in the project directory
- Check the filename is correct

**Error: "Unexpected token"**
- Check syntax (semicolons, braces)
- See LANGUAGE_SPEC.md for correct syntax

**Error: "Variable not declared"**
- Declare variables before using them
- Check spelling

### 10. Next Steps

1. Read LANGUAGE_SPEC.md for complete syntax
2. Try modifying test files
3. Create your own recipes
4. Explore the compiler phases
5. Read PROJECT_DOCUMENTATION.md for technical details

---

**That's it! You're ready to use RecipeScript!** 🎉

For questions, see the documentation files or examine the source code.
