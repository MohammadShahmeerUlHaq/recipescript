"""
Quick verification script to check specific parsing table entries
"""

from ll1_parser_generator import define_recipescript_grammar

# Create parser
parser = define_recipescript_grammar()

# Compute all sets
parser.compute_nullable()
parser.compute_first()
parser.compute_follow('<program>')
parser.build_parsing_table()

print("=" * 70)
print("VERIFICATION: <arg_list> Production")
print("=" * 70)

print("\n1. Grammar for <arg_list>:")
for prod in parser.grammar['<arg_list>']:
    print(f"   <arg_list> → {' '.join(prod)}")

print("\n2. NULLABLE(<arg_list>):", parser.nullable.get('<arg_list>', False))

print("\n3. FIRST(<arg_list>):", sorted(parser.first['<arg_list>']))

print("\n4. FOLLOW(<arg_list>):", sorted(parser.follow['<arg_list>']))

print("\n5. Parsing Table entries for <arg_list>:")
for terminal in sorted(parser.terminals):
    productions = parser.parsing_table['<arg_list>'].get(terminal, [])
    if productions:
        for prod in productions:
            prod_str = ' '.join(prod).replace('ε', 'ε')
            print(f"   Table[<arg_list>][{terminal:15}] = <arg_list> → {prod_str}")

print("\n" + "=" * 70)
print("VERIFICATION: Epsilon Productions")
print("=" * 70)

epsilon_nts = [nt for nt in parser.non_terminals if parser.nullable.get(nt, False)]
print(f"\nNullable non-terminals ({len(epsilon_nts)}):")
for nt in sorted(epsilon_nts):
    print(f"  - {nt}")
    # Check if epsilon production exists in table for FOLLOW set
    follow_set = parser.follow[nt]
    for terminal in sorted(follow_set):
        if terminal in parser.terminals:
            productions = parser.parsing_table[nt].get(terminal, [])
            epsilon_prods = [p for p in productions if len(p) == 1 and p[0] == 'ε']
            if epsilon_prods:
                print(f"    ✓ Table[{nt}][{terminal}] has ε production")

print("\n" + "=" * 70)
print("VERIFICATION: Sample Entries")
print("=" * 70)

# Check some key entries
test_cases = [
    ('<arg_list>', ')'),
    ('<arg_list>', 'NUMBER'),
    ('<arg_list>', 'IDENTIFIER'),
    ('<param_list>', ')'),
    ('<param_list>', 'ingredient'),
    ('<value_tail>', ';'),
    ('<value_tail>', 'cups'),
    ('<expression_prime>', ';'),
    ('<expression_prime>', '+'),
    ('<term_prime>', '+'),
    ('<term_prime>', '*'),
]

for nt, terminal in test_cases:
    productions = parser.parsing_table[nt].get(terminal, [])
    if productions:
        for prod in productions:
            prod_str = ' '.join(prod).replace('ε', 'ε')
            print(f"✓ Table[{nt:20}][{terminal:15}] = {nt} → {prod_str}")
    else:
        print(f"✗ Table[{nt:20}][{terminal:15}] = EMPTY")

print("\n" + "=" * 70)
