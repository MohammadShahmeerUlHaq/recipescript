# RecipeScript Compiler

A domain-specific language (DSL) compiler for cooking recipe automation and meal planning.

**Status: ✅ COMPLETE AND TESTED - All 6 Tests Passing**

---

## 🎯 Project Overview

RecipeScript is a complete compiler implementation for CS4031 Compiler Construction course. It demonstrates all six phases of compilation for a practical, domain-specific language designed for cooking recipes.

### Why RecipeScript?

- **Unique Domain**: Cooking recipe automation (completely different from typical languages)
- **Natural Syntax**: Easy-to-read commands like "mix flour with sugar"
- **Type Safety**: Domain-specific validation (temperature ranges, ingredient types)
- **Practical Application**: Real-world use in smart kitchens and meal planning

---

## 🚀 Quick Start

### Run a Test Recipe
```bash
python recipescript.py tests/test1.recipe
```

### Run All Tests
```bash
cd tests
python run_all_tests.py
```
**Result: ✅ 6/6 tests passing**

### Interactive Mode
```bash
python recipescript.py
>>> ingredient flour = 2 cups;
>>> serve "Hello RecipeScript!";
>>> exit
```

### Try Example Recipes
```bash
python recipescript.py examples/chocolate_cookies.recipe
python recipescript.py examples/pasta.recipe
python recipescript.py examples/bread.recipe
```

---

## 📝 Language Features

### Data Types
```recipe
ingredient flour = 2 cups;      # Food ingredients with quantities
temp oven = 350 F;              # Temperature (F or C)
time duration = 30 minutes;     # Time duration
quantity servings = 4;          # Numeric quantities
text message = "Ready!";        # Text strings
```

### Operations
```recipe
mix flour with sugar with butter;   # Combine ingredients
heat oven to 350 F;                 # Set temperature
wait 15 minutes;                    # Timing control
serve "Cookies ready!";             # Output message
scale flour by 2;                   # Adjust quantities
add sugar to flour;                 # Add ingredient
```

### Control Flow
```recipe
# Repeat loops
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

### Units Supported
- **Volume**: cups, tbsp, tsp, ml, oz
- **Weight**: grams, lbs
- **Temperature**: F (Fahrenheit), C (Celsius)
- **Time**: minutes, seconds, hours

---

## 🏗️ Compiler Architecture

### All 6 Phases Implemented:

1. **Lexical Analysis** (`lexer.py` - 250 lines)
   - Tokenization with unit recognition
   - Multi-character operators
   - Comment handling
   - Line/column tracking

2. **Syntax Analysis** (`parser.py` - 400 lines)
   - Recursive descent parser
   - AST construction
   - Natural language syntax support
   - Error recovery

3. **Semantic Analysis** (`semantic_analyzer.py` - 200 lines)
   - Symbol table with scoping
   - Type checking
   - Domain validation (temp ranges, etc.)
   - Semantic error detection

4. **Intermediate Code** (`intermediate_code.py` - 250 lines)
   - Three-address code generation
   - Temporary variables
   - Label management
   - Control flow translation

5. **Optimization** (`optimizer.py` - 150 lines)
   - Constant folding
   - Dead code elimination
   - Extensible framework

6. **Code Generation** (`code_generator.py` - 200 lines)
   - TAC interpreter
   - Variable storage
   - Control flow execution
   - Recipe operation execution

**Total: ~1,720 lines of code**

---

## 📚 Documentation

| File | Description |
|------|-------------|
| **README.md** | This file - project overview |
| **QUICKSTART.md** | Get started in 5 minutes |
| **LANGUAGE_SPEC.md** | Complete language specification with BNF grammar |
| **PROJECT_DOCUMENTATION.md** | Detailed technical documentation |
| **HANDWRITTEN_GUIDE.md** | Guide for creating required handwritten artifacts |
| **SUBMISSION_CHECKLIST.md** | Complete submission checklist |
| **reflection.md** | Project reflection (what learned, challenges, improvements) |

---

## ✅ Test Cases

All 6 test cases pass successfully:

| Test | Description | Features Tested |
|------|-------------|-----------------|
| **test1.recipe** | Simple cookie recipe | Basic declarations, mixing, heating, timing |
| **test2.recipe** | Scaled recipe | Scaling operation, quantity manipulation |
| **test3.recipe** | Conditional cooking | When/then/else, comparisons |
| **test4.recipe** | Repeated steps | Repeat loops, iteration |
| **test5.recipe** | Complex operations | Multiple ingredients, mixing, adding |
| **test6.recipe** | Units and timing | Celsius, grams, different units |

---

## 🎓 For Course Submission

### ✅ Completed:
- [x] Unique language design (RecipeScript)
- [x] Complete BNF grammar specification
- [x] All 6 compiler phases implemented
- [x] 6 comprehensive test cases (all passing)
- [x] Complete documentation
- [x] Project reflection
- [x] Working interactive mode

### ⚠️ Required (You Must Do):
- [ ] **Create handwritten artifacts** (see HANDWRITTEN_GUIDE.md)
  - DFA for token recognition
  - Parse trees (minimum 2)
  - Symbol table examples
- [ ] **Print and annotate code**
- [ ] **Practice demonstration**

---

## 🎯 Example Recipe

```recipe
# Chocolate Chip Cookies
ingredient flour = 2 cups;
ingredient sugar = 1 cups;
ingredient butter = 0.5 cups;
ingredient chocolate_chips = 1 cups;
temp oven = 350 F;

# Preheat oven
heat oven to 350 F;
wait 10 minutes;

# Mix ingredients
mix flour with sugar;
mix flour with butter;
add chocolate_chips to flour;

# Bake
wait 15 minutes;
serve "Cookies are ready!";
```

**Output:**
```
Heating oven to 350 fahrenheit
Waiting for 10 minutes
Mixing: flour, sugar
Mixing: flour, butter
Adding chocolate_chips to flour
Waiting for 15 minutes
Cookies are ready!
```

---

## 🔧 Project Structure

```
recipescript-compiler/
├── recipescript.py              # Main entry point - Run this!
├── README.md                    # This file
│
├── src/                         # Source code (1,720 lines)
│   ├── compiler.py              # Main compiler (150 lines)
│   ├── lexer.py                 # Phase 1: Lexical analysis (250 lines)
│   ├── parser.py                # Phase 2: Syntax analysis (400 lines)
│   ├── semantic_analyzer.py     # Phase 3: Semantic analysis (200 lines)
│   ├── intermediate_code.py     # Phase 4: TAC generation (250 lines)
│   ├── optimizer.py             # Phase 5: Optimization (150 lines)
│   ├── code_generator.py        # Phase 6: Code generation (200 lines)
│   └── token_types.py           # Token definitions (120 lines)
│
├── tests/                       # Test files
│   ├── test1.recipe             # Test: Simple recipe
│   ├── test2.recipe             # Test: Scaling
│   ├── test3.recipe             # Test: Conditionals
│   ├── test4.recipe             # Test: Loops
│   ├── test5.recipe             # Test: Complex operations
│   ├── test6.recipe             # Test: Units
│   └── run_all_tests.py         # Test runner
│
├── examples/                    # Example recipes
│   ├── chocolate_cookies.recipe # Chocolate chip cookies
│   ├── pasta.recipe             # Simple pasta dish
│   └── bread.recipe             # Homemade bread
│
└── docs/                        # Documentation
    ├── QUICKSTART.md            # Quick start guide
    ├── LANGUAGE_SPEC.md         # Language specification
    ├── PROJECT_DOCUMENTATION.md # Technical documentation
    ├── HANDWRITTEN_GUIDE.md     # Handwritten artifacts guide
    ├── PROJECT_COMPLETE.md      # Completion summary
    └── reflection.md            # Project reflection
```

---

## 🌟 What Makes RecipeScript Unique

### Compared to Similar Projects:

| Feature | RecipeScript | Typical Languages |
|---------|--------------|-------------------|
| **Domain** | Cooking recipes | General purpose |
| **Keywords** | mix, heat, serve, wait | print, if, while |
| **Types** | ingredient, temp, time | int, float, string |
| **Syntax** | Natural language | C-like |
| **Units** | Built-in (cups, F, minutes) | None |
| **Validation** | Domain-specific (temp ranges) | Generic |

### Key Innovations:
1. **Natural language syntax** - "mix flour with sugar"
2. **Domain-specific types** - ingredient, temp, time
3. **Built-in unit system** - cups, F, minutes, etc.
4. **Recipe operations** - mix, heat, wait, serve, scale
5. **Safety validation** - Temperature ranges, positive values
6. **Practical application** - Real-world cooking automation

---

## 💡 Usage Examples

### Command Line
```bash
# Compile and run a recipe
python recipescript.py my_recipe.recipe

# See all 6 phases
python recipescript.py tests/test1.recipe

# Run test suite
cd tests
python run_all_tests.py

# Try examples
python recipescript.py examples/chocolate_cookies.recipe
```

### Interactive REPL
```bash
python recipescript.py
>>> ingredient pasta = 500 grams;
>>> temp water = 212 F;
>>> heat water to 212 F;
>>> wait 10 minutes;
>>> serve "Pasta ready!";
>>> exit
```

---

## 📖 Learning Resources

1. **Start Here**: Read QUICKSTART.md
2. **Language Reference**: See LANGUAGE_SPEC.md
3. **Technical Details**: Read PROJECT_DOCUMENTATION.md
4. **Handwritten Work**: Follow HANDWRITTEN_GUIDE.md
5. **Reflection**: Read reflection.md

---

## 🎓 Educational Value

This project demonstrates:
- **Compiler Theory**: Lexical analysis, parsing, semantic analysis, code generation
- **Language Design**: Domain-specific languages, syntax design, type systems
- **Software Engineering**: Modular design, testing, documentation
- **Problem Solving**: Error handling, optimization, practical applications

---

## 🚀 Future Enhancements

Potential improvements:
- Functions/procedures for reusable recipes
- Unit conversion automation
- Nutritional calculation
- Shopping list generation
- Recipe import/export
- Smart kitchen device integration
- Parallel step execution
- Recipe optimization

---

## 📊 Project Statistics

- **Lines of Code**: ~1,720
- **Files**: 21
- **Test Cases**: 6 (all passing)
- **Documentation Pages**: 7
- **Compiler Phases**: 6 (all implemented)
- **Time Invested**: ~12 hours
- **Status**: ✅ Complete and ready for submission

---

## 🎯 Success Criteria

✅ **All Requirements Met:**
- Unique language design
- Complete BNF grammar
- All 6 compiler phases
- Working implementation
- Comprehensive testing
- Professional documentation
- Project reflection

**Ready for demonstration and submission!**

---

## 📞 Support

For questions or issues:
1. Check QUICKSTART.md for common problems
2. Read LANGUAGE_SPEC.md for syntax reference
3. See PROJECT_DOCUMENTATION.md for technical details
4. Review test files for examples

---

**RecipeScript - Making Cooking Computable** 🍳👨‍💻

*A complete compiler implementation demonstrating all phases of compilation for a practical domain-specific language.*

