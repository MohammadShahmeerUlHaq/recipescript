# Getting Started with RecipeScript

## 📦 Installation

No installation required! Just Python 3.x.

## 🚀 Quick Start (30 seconds)

### 1. Test the Compiler
```bash
python recipescript.py tests/test1.recipe
```

You should see all 6 compiler phases execute successfully!

### 2. Run All Tests
```bash
cd tests
python run_all_tests.py
```

Expected result: **✅ 6/6 tests passing**

### 3. Try an Example Recipe
```bash
python recipescript.py examples/chocolate_cookies.recipe
```

### 4. Interactive Mode
```bash
python recipescript.py
```

Then type:
```recipe
>>> ingredient flour = 2 cups;
>>> temp oven = 350 F;
>>> heat oven to 350 F;
>>> serve "Hello RecipeScript!";
>>> exit
```

## 📁 Project Structure

```
recipescript-compiler/
├── recipescript.py          # ← Run this file!
├── README.md                # Main documentation
│
├── src/                     # Compiler source code
│   ├── compiler.py          # Main compiler
│   ├── lexer.py             # Phase 1: Lexical Analysis
│   ├── parser.py            # Phase 2: Syntax Analysis
│   ├── semantic_analyzer.py # Phase 3: Semantic Analysis
│   ├── intermediate_code.py # Phase 4: Intermediate Code
│   ├── optimizer.py         # Phase 5: Optimization
│   ├── code_generator.py    # Phase 6: Code Generation
│   └── token_types.py       # Token definitions
│
├── tests/                   # Test files
│   ├── test1.recipe - test6.recipe
│   └── run_all_tests.py
│
├── examples/                # Example recipes
│   ├── chocolate_cookies.recipe
│   ├── pasta.recipe
│   └── bread.recipe
│
└── docs/                    # Documentation
    ├── QUICKSTART.md
    ├── LANGUAGE_SPEC.md
    ├── PROJECT_DOCUMENTATION.md
    ├── HANDWRITTEN_GUIDE.md
    └── reflection.md
```

## 📖 Usage Examples

### Run a Recipe File
```bash
python recipescript.py path/to/recipe.recipe
```

### See All Compiler Phases
```bash
python recipescript.py tests/test1.recipe
```

This shows:
1. Lexical Analysis (tokenization)
2. Syntax Analysis (AST building)
3. Semantic Analysis (type checking)
4. Intermediate Code (TAC generation)
5. Optimization
6. Code Execution

### Create Your Own Recipe

Create `my_recipe.recipe`:
```recipe
# My First Recipe
ingredient pasta = 500 grams;
temp water = 212 F;

heat water to 212 F;
wait 5 minutes;
mix pasta with water;
wait 10 minutes;
serve "Pasta is ready!";
```

Run it:
```bash
python recipescript.py my_recipe.recipe
```

## 🎯 Language Basics

### Data Types
```recipe
ingredient flour = 2 cups;      # Ingredients with quantities
temp oven = 350 F;              # Temperature (F or C)
time duration = 30 minutes;     # Time duration
quantity servings = 4;          # Numeric quantities
text message = "Ready!";        # Text strings
```

### Operations
```recipe
mix flour with sugar;           # Combine ingredients
heat oven to 350 F;             # Set temperature
wait 15 minutes;                # Timing control
serve "Done!";                  # Output message
scale flour by 2;               # Adjust quantities
add sugar to flour;             # Add ingredient
```

### Control Flow
```recipe
# Loops
repeat 3 times {
    mix dough;
    wait 5 minutes;
}

# Conditionals
when temp < 350 then {
    heat oven to 350 F;
} else {
    serve "Already hot!";
}
```

### Units
- **Volume**: cups, tbsp, tsp, ml, oz
- **Weight**: grams, lbs
- **Temperature**: F (Fahrenheit), C (Celsius)
- **Time**: minutes, seconds, hours

## 📚 Documentation

| File | Description |
|------|-------------|
| **README.md** | Main project overview |
| **docs/QUICKSTART.md** | Quick start guide |
| **docs/LANGUAGE_SPEC.md** | Complete language specification |
| **docs/PROJECT_DOCUMENTATION.md** | Technical documentation |
| **docs/HANDWRITTEN_GUIDE.md** | Guide for handwritten artifacts |
| **docs/reflection.md** | Project reflection |

## 🎓 For Course Submission

### What's Complete ✅
- All 6 compiler phases implemented
- 6 test cases (all passing)
- Complete documentation
- Example recipes
- Interactive mode

### What You Need to Do ⚠️
1. **Create handwritten artifacts** (see `docs/HANDWRITTEN_GUIDE.md`)
   - DFAs for token recognition
   - Parse trees (minimum 2)
   - Symbol table examples
   
2. **Print and annotate code**
   - Print all files in `src/` folder
   - Add handwritten notes

3. **Practice demonstration**
   - Run test cases
   - Explain each phase

## 🔧 Troubleshooting

### "File not found" error
Make sure you're in the project root directory:
```bash
cd path/to/recipescript-compiler
python recipescript.py tests/test1.recipe
```

### "Module not found" error
The imports are configured correctly. Make sure you're running `recipescript.py` from the root directory.

### Tests not passing
Run from the tests directory:
```bash
cd tests
python run_all_tests.py
```

## 🎉 Next Steps

1. ✅ Test the compiler (you just did!)
2. 📖 Read `docs/QUICKSTART.md` for language details
3. 🧪 Try modifying test files
4. 🍳 Create your own recipes
5. 📚 Read `docs/LANGUAGE_SPEC.md` for complete reference
6. ✍️ Create handwritten artifacts (see `docs/HANDWRITTEN_GUIDE.md`)

## 💡 Tips

- Start with simple recipes (like test1.recipe)
- Use comments (#) to document your recipes
- Check example recipes for inspiration
- All statements must end with semicolon (;)
- Use natural language syntax: "mix flour with sugar"

## 🆘 Need Help?

1. Check `docs/QUICKSTART.md` for common issues
2. See `docs/LANGUAGE_SPEC.md` for syntax reference
3. Look at test files for examples
4. Read `docs/PROJECT_DOCUMENTATION.md` for technical details

---

**You're all set! Start cooking with code!** 🍳👨‍💻
