# ✍️ Handwritten Work - What You Must Create

## ⚠️ IMPORTANT: This is the ONLY remaining work

Everything else is complete. You just need to create these handwritten artifacts.

---

## 📋 Quick Summary

**Total Time Needed:** 2-3 hours  
**Reference Guide:** `docs/HANDWRITTEN_GUIDE.md`  
**Materials Needed:** Paper, pen, ruler, scanner/camera

---

## 1️⃣ Lexical Analysis Artifacts (30-45 minutes)

### What to Draw:

#### A. DFA for Identifier Recognition
```
Draw a state diagram with circles and arrows:

States: q0 (start), q1 (accepting - double circle)

Transitions:
- q0 → q1 on [a-z, A-Z, _]
- q1 → q1 on [a-z, A-Z, 0-9, _]

Example: Draw circles for states, arrows for transitions
Label each arrow with the character class
```

#### B. DFA for Number Recognition
```
Draw a state diagram:

States: q0 (start), q1 (integer - accepting), 
        q2 (decimal point), q3 (float - accepting)

Transitions:
- q0 → q1 on [0-9]
- q1 → q1 on [0-9]
- q1 → q2 on [.]
- q2 → q3 on [0-9]
- q3 → q3 on [0-9]
```

#### C. Transition Table
```
Draw a table:

| State | [a-z,A-Z,_] | [0-9] | Other |
|-------|-------------|-------|-------|
| q0    | q1          | -     | error |
| q1    | q1          | q1    | accept|
```

#### D. Regular Expressions
```
Write these by hand:

Identifier: [a-zA-Z_][a-zA-Z0-9_]*
Integer: [0-9]+
Float: [0-9]+\.[0-9]+
String: "[^"]*"
Comment: #[^\n]*
```

**Reference:** Section 1 of `docs/HANDWRITTEN_GUIDE.md`

---

## 2️⃣ Syntax Analysis Artifacts (45-60 minutes)

### What to Draw:

#### A. Parse Tree 1: Input Statement
```
Code: input servings;

Draw tree structure:

                <program>
                    |
              <statement_list>
                    |
                <statement>
                    |
            <input_stmt> ;
                    |
        input <identifier>
                 |
              servings

Use boxes or circles for nodes
Draw lines connecting parent to children
Label each node clearly
```

#### B. Parse Tree 2: Declaration with Expression
```
Code: ingredient flour = 0.5 * servings cups;

Draw tree structure:

                <program>
                    |
              <statement_list>
                    |
                <statement>
                    |
            <declaration> ;
                    |
        <type> <identifier> = <value>
          |        |              |
     ingredient  flour    <expression> <unit>
                               |         |
                          <term> * <factor>  cups
                            |        |
                           0.5    servings
```

#### C. Parse Tree 3: Declaration Statement
```
Code: ingredient flour = 2 cups;

Draw tree structure:

                <program>
                    |
              <statement_list>
                    |
                <statement>
                    |
            <declaration> ;
                    |
        <type> <identifier> = <value>
          |        |              |
     ingredient  flour    <number> <unit>
                             |       |
                             2      cups

Use boxes or circles for nodes
Draw lines connecting parent to children
Label each node clearly
```

#### D. Parse Tree 4: Mix Operation
```
Code: mix flour with sugar with butter;

Draw tree structure:

                <program>
                    |
              <statement_list>
                    |
                <statement>
                    |
              <operation> ;
                    |
            <mix_operation>
                    |
        mix <ingredient_list>
                    |
        <identifier> with <ingredient_list>
            |                    |
          flour      <identifier> with <identifier>
                         |                |
                       sugar            butter

Draw this as a tree with proper branching
```

#### C. Leftmost Derivation
```
Show step-by-step derivation for: ingredient flour = 2 cups;

Write each step:

<program>
=> <statement_list>
=> <statement>
=> <declaration> ;
=> <type> <identifier> = <value> ;
=> ingredient <identifier> = <value> ;
=> ingredient flour = <value> ;
=> ingredient flour = <number> <unit> ;
=> ingredient flour = 2 <unit> ;
=> ingredient flour = 2 cups ;

Use => to show derivation steps
Underline the non-terminal being expanded
```

#### D. Grammar Rules (BNF)
```
Write these grammar rules by hand:

<program> ::= <statement_list>
<statement> ::= <declaration> ";" | <operation> ";"
<declaration> ::= <type> <identifier> "=" <value>
<type> ::= "ingredient" | "time" | "temp" | "quantity"
<value> ::= <number> <unit> | <number>
<operation> ::= "mix" <ingredient_list>
              | "heat" <identifier> "to" <value>
              | "wait" <time_value>
              | "serve" <string>
```

**Reference:** Section 2 of `docs/HANDWRITTEN_GUIDE.md`

---

## 3️⃣ Semantic Analysis Artifacts (30-45 minutes)

### What to Draw:

#### A. Symbol Table (Simple)
```
For this code:
ingredient flour = 2 cups;
temp oven = 350 F;
ingredient sugar = 1 cups;

Draw table:

+-------------+------------+-------+------+
| Name        | Type       | Scope | Line |
+-------------+------------+-------+------+
| flour       | ingredient | 0     | 1    |
| oven        | temp       | 0     | 2    |
| sugar       | ingredient | 0     | 3    |
+-------------+------------+-------+------+

Use ruler to draw straight lines
Make columns clear
Fill in all information
```

#### B. Symbol Table with Scopes
```
For this code:
ingredient flour = 2 cups;
repeat 3 times {
    ingredient temp_flour = 1 cups;
    mix temp_flour;
}

Draw table showing scope levels:

+-------------+------------+-------+------+
| Name        | Type       | Scope | Line |
+-------------+------------+-------+------+
| flour       | ingredient | 0     | 1    |
| temp_flour  | ingredient | 1     | 3    |
+-------------+------------+-------+------+

Add note: "After exiting repeat block, temp_flour is removed"
```

#### C. Type Checking Examples
```
Write these examples:

Example 1 (Valid):
ingredient flour = 2 cups;
✓ Type: ingredient, Value: 2 cups

Example 2 (Invalid - Range):
temp oven = 600 F;
✗ Error: Temperature out of range (0-500F)

Example 3 (Invalid - Undeclared):
mix flour with sugar;
✗ Error: 'sugar' not declared
```

#### D. Semantic Rules
```
Write these rules:

1. Variables must be declared before use
2. Temperature range: 0-500°F or 0-260°C
3. Time and quantity must be positive
4. Only ingredients can be mixed
5. Type compatibility in operations
```

**Reference:** Section 3 of `docs/HANDWRITTEN_GUIDE.md`

---

## 📸 After Creating Artifacts

### Scanning/Photographing

1. **Use good lighting**
2. **Ensure all text is readable**
3. **Scan at 300 DPI or higher**
4. **Or take clear photos with phone**
5. **Save as PDF or high-quality images**

### Labeling

Label each artifact clearly:
- "DFA for Identifier Recognition"
- "Parse Tree for Declaration"
- "Symbol Table with Scopes"
- etc.

### Organization

Create a folder:
```
handwritten_artifacts/
├── lexical_dfa_identifier.pdf
├── lexical_dfa_number.pdf
├── lexical_transition_table.pdf
├── syntax_parse_tree_1.pdf
├── syntax_parse_tree_2.pdf
├── syntax_derivation.pdf
├── semantic_symbol_table.pdf
├── semantic_symbol_table_scopes.pdf
└── semantic_type_checking.pdf
```

---

## ✅ Checklist

### Lexical Analysis
- [ ] DFA for identifier recognition (drawn)
- [ ] DFA for number recognition (drawn)
- [ ] Transition table (drawn)
- [ ] Regular expressions (written)
- [ ] All scanned/photographed
- [ ] All labeled

### Syntax Analysis
- [ ] Parse tree 1: declaration (drawn)
- [ ] Parse tree 2: mix operation (drawn)
- [ ] Leftmost derivation (written)
- [ ] Grammar rules (written)
- [ ] All scanned/photographed
- [ ] All labeled

### Semantic Analysis
- [ ] Symbol table simple (drawn)
- [ ] Symbol table with scopes (drawn)
- [ ] Type checking examples (written)
- [ ] Semantic rules (written)
- [ ] All scanned/photographed
- [ ] All labeled

### Final Steps
- [ ] All artifacts in one folder
- [ ] All clearly labeled
- [ ] All readable
- [ ] Ready to include in submission

---

## 💡 Tips

1. **Use pencil first, then pen** - Easier to correct mistakes
2. **Use ruler for straight lines** - Makes diagrams neat
3. **Label everything clearly** - States, transitions, nodes
4. **Add explanations** - Brief notes help understanding
5. **Take your time** - Quality matters more than speed
6. **Check readability** - Make sure scans are clear

---

## 📚 Reference

**Complete Guide:** `docs/HANDWRITTEN_GUIDE.md`

This file has:
- Detailed instructions for each artifact
- More examples
- Templates
- Grading criteria
- Tips and tricks

---

## ⏱️ Time Estimate

- **Lexical artifacts:** 30-45 minutes
- **Syntax artifacts:** 45-60 minutes
- **Semantic artifacts:** 30-45 minutes
- **Scanning/organizing:** 15-30 minutes

**Total: 2-3 hours**

---

## 🎯 This is ALL You Need to Do

Everything else is complete:
- ✅ All code written and tested
- ✅ All documentation complete
- ✅ All tests passing
- ✅ Project organized
- ✅ Reflection written

**Just create these handwritten artifacts and you're done!**

---

## 📞 Quick Reference

**Where to find examples:** `docs/HANDWRITTEN_GUIDE.md`  
**What to draw:** This file (above)  
**How long:** 2-3 hours  
**When to do:** Before submission deadline

---

**Good luck! You've got this!** ✍️📝
