"""
Generate comprehensive compilation report for comprehensive_example.recipe
Shows all phases: Lexer, Parser, Semantic Analysis, TAC, Optimization, Execution
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from lexer import Lexer
from parser import Parser
from semantic_analyzer import SemanticAnalyzer
from intermediate_code import IntermediateCodeGenerator
from optimizer import Optimizer
from code_generator import CodeGenerator

def generate_report(source_file, output_file, input_value="12"):
    """Generate complete compilation report"""
    
    # Read source code
    with open(source_file, 'r') as f:
        source_code = f.read()
    
    with open(output_file, 'w', encoding='utf-8') as out:
        out.write("=" * 80 + "\n")
        out.write("COMPREHENSIVE COMPILATION REPORT\n")
        out.write("RecipeScript Compiler - All Phases\n")
        out.write("=" * 80 + "\n\n")
        
        out.write(f"Source File: {source_file}\n")
        out.write(f"Input Value: {input_value}\n")
        out.write("=" * 80 + "\n\n")
        
        # PHASE 1: LEXICAL ANALYSIS
        out.write("=" * 80 + "\n")
        out.write("PHASE 1: LEXICAL ANALYSIS (TOKENIZATION)\n")
        out.write("=" * 80 + "\n\n")
        
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        
        out.write(f"Total Tokens Generated: {len(tokens)}\n\n")
        out.write("Token List:\n")
        out.write("-" * 80 + "\n")
        for i, token in enumerate(tokens, 1):
            out.write(f"{i:4}. {token}\n")
        
        # PHASE 2: SYNTAX ANALYSIS
        out.write("\n" + "=" * 80 + "\n")
        out.write("PHASE 2: SYNTAX ANALYSIS (PARSING)\n")
        out.write("=" * 80 + "\n\n")
        
        parser = Parser(tokens)
        ast = parser.parse()
        
        out.write(f"Recipes Parsed: {len(ast.recipes)}\n")
        out.write(f"Main Statements: {len(ast.statements)}\n\n")
        
        out.write("Recipe Declarations:\n")
        out.write("-" * 80 + "\n")
        for recipe in ast.recipes:
            out.write(f"Recipe: {recipe.name}\n")
            out.write(f"  Parameters: {len(recipe.params)}\n")
            for param in recipe.params:
                out.write(f"    - {param['name']}: {param['type']}\n")
            out.write(f"  Return Type: {recipe.return_type}\n")
            out.write(f"  Body Statements: {len(recipe.body)}\n\n")
        
        out.write("Abstract Syntax Tree (AST) - Detailed Structure:\n")
        out.write("-" * 80 + "\n")
        
        def print_ast_node(node, indent=0, prefix="", is_last=False, out_file=out):
            """Recursively print AST structure with perfect indentation"""
            # Build the proper indentation string based on tree structure
            indent_str = ""
            node_type = type(node).__name__
            
            if node_type == "Program":
                out_file.write(f"Program\n")
                out_file.write(f"├── RecipeList ({len(node.recipes)} recipe{'s' if len(node.recipes) != 1 else ''})\n")
                for i, recipe in enumerate(node.recipes):
                    recipe_is_last = (i == len(node.recipes) - 1)
                    print_ast_node(recipe, 1, "│   ", recipe_is_last, out_file)
                out_file.write(f"└── MainBlock ({len(node.statements)} statements)\n")
                for i, stmt in enumerate(node.statements):
                    stmt_is_last = (i == len(node.statements) - 1)
                    print_ast_node(stmt, 1, "    ", stmt_is_last, out_file)
            
            elif node_type == "RecipeDeclaration":
                connector = "└── " if is_last else "├── "
                out_file.write(f"{prefix}{connector}RecipeDeclaration\n")
                continuation = "    " if is_last else "│   "
                out_file.write(f"{prefix}{continuation}├── Name: {node.name}\n")
                out_file.write(f"{prefix}{continuation}├── Parameters ({len(node.params)})\n")
                for i, param in enumerate(node.params):
                    param_type = str(param['type']).split('.')[-1]
                    param_is_last = (i == len(node.params) - 1)
                    param_connector = "└── " if param_is_last else "├── "
                    out_file.write(f"{prefix}{continuation}│   {param_connector}Parameter(name=\"{param['name']}\", type={param_type})\n")
                out_file.write(f"{prefix}{continuation}├── ReturnType: {str(node.return_type).split('.')[-1] if node.return_type else 'None'}\n")
                out_file.write(f"{prefix}{continuation}└── Body (StatementList: {len(node.body)} statements)\n")
                for i, stmt in enumerate(node.body):
                    stmt_is_last = (i == len(node.body) - 1)
                    print_ast_node(stmt, indent + 1, prefix + continuation + "    ", stmt_is_last, out_file)
            
            elif node_type == "Declaration":
                var_type = str(node.var_type).split('.')[-1]
                connector = "└── " if is_last else "├── "
                out_file.write(f"{prefix}{connector}DeclarationStatement\n")
                continuation = "    " if is_last else "│   "
                out_file.write(f"{prefix}{continuation}├── Variable: {node.name}\n")
                out_file.write(f"{prefix}{continuation}├── Type: {var_type}\n")
                out_file.write(f"{prefix}{continuation}└── Value (Expression):\n")
                out_file.write(f"{prefix}{continuation}    ")
                print_ast_value(node.value, out_file)
                out_file.write("\n")
            
            elif node_type == "InputStatement":
                connector = "└── " if is_last else "├── "
                out_file.write(f"{prefix}{connector}InputStatement\n")
                continuation = "    " if is_last else "│   "
                out_file.write(f"{prefix}{continuation}└── Variable (Identifier): {node.var_name}\n")
            
            elif node_type == "Assignment":
                connector = "└── " if is_last else "├── "
                out_file.write(f"{prefix}{connector}AssignmentStatement\n")
                continuation = "    " if is_last else "│   "
                out_file.write(f"{prefix}{continuation}├── Target: {node.name}\n")
                out_file.write(f"{prefix}{continuation}└── Value (Expression): ")
                print_ast_value(node.value, out_file)
                out_file.write("\n")
            
            elif node_type == "WhenStatement":
                connector = "└── " if is_last else "├── "
                out_file.write(f"{prefix}{connector}WhenStatement\n")
                continuation = "    " if is_last else "│   "
                out_file.write(f"{prefix}{continuation}├── Condition (Expression):\n")
                out_file.write(f"{prefix}{continuation}│   ")
                print_ast_value(node.condition, out_file)
                out_file.write("\n")
                
                # Print then body statements
                if node.else_body:
                    out_file.write(f"{prefix}{continuation}├── ThenBlock (StatementList: {len(node.then_body)} statement{'s' if len(node.then_body) != 1 else ''})\n")
                    then_continuation = "│   "
                else:
                    out_file.write(f"{prefix}{continuation}└── ThenBlock (StatementList: {len(node.then_body)} statement{'s' if len(node.then_body) != 1 else ''})\n")
                    then_continuation = "    "
                
                for i, stmt in enumerate(node.then_body):
                    stmt_is_last = (i == len(node.then_body) - 1)
                    print_ast_node(stmt, indent + 1, prefix + continuation + then_continuation, stmt_is_last, out_file)
                
                # Print else body if exists
                if node.else_body:
                    out_file.write(f"{prefix}{continuation}└── ElseBlock (StatementList: {len(node.else_body)} statement{'s' if len(node.else_body) != 1 else ''})\n")
                    for i, stmt in enumerate(node.else_body):
                        stmt_is_last = (i == len(node.else_body) - 1)
                        print_ast_node(stmt, indent + 1, prefix + continuation + "    ", stmt_is_last, out_file)
            
            elif node_type == "RepeatStatement":
                connector = "└── " if is_last else "├── "
                out_file.write(f"{prefix}{connector}RepeatStatement\n")
                continuation = "    " if is_last else "│   "
                out_file.write(f"{prefix}{continuation}├── Count (Expression): Literal({node.count})\n")
                out_file.write(f"{prefix}{continuation}└── Body (StatementList: {len(node.body)} statement{'s' if len(node.body) != 1 else ''})\n")
                for i, stmt in enumerate(node.body):
                    stmt_is_last = (i == len(node.body) - 1)
                    print_ast_node(stmt, indent + 1, prefix + continuation + "    ", stmt_is_last, out_file)
            
            elif node_type == "ServeOperation":
                connector = "└── " if is_last else "├── "
                out_file.write(f"{prefix}{connector}ServeStatement\n")
                continuation = "    " if is_last else "│   "
                out_file.write(f"{prefix}{continuation}└── Message (StringLiteral): \"{node.message}\"\n")
            
            elif node_type == "DisplayOperation":
                connector = "└── " if is_last else "├── "
                out_file.write(f"{prefix}{connector}DisplayStatement\n")
                continuation = "    " if is_last else "│   "
                out_file.write(f"{prefix}{continuation}└── Variable (Identifier): {node.variable}\n")
            
            elif node_type == "MixOperation":
                connector = "└── " if is_last else "├── "
                out_file.write(f"{prefix}{connector}MixStatement\n")
                continuation = "    " if is_last else "│   "
                out_file.write(f"{prefix}{continuation}└── Ingredients (IdentifierList)\n")
                for i, ing in enumerate(node.ingredients):
                    ing_is_last = (i == len(node.ingredients) - 1)
                    ing_connector = "└── " if ing_is_last else "├── "
                    out_file.write(f"{prefix}{continuation}    {ing_connector}Identifier: {ing}\n")
            
            elif node_type == "WaitOperation":
                connector = "└── " if is_last else "├── "
                out_file.write(f"{prefix}{connector}WaitStatement\n")
                continuation = "    " if is_last else "│   "
                out_file.write(f"{prefix}{continuation}└── Duration (Expression):\n")
                out_file.write(f"{prefix}{continuation}    ")
                print_ast_value(node.duration, out_file)
                out_file.write("\n")
            
            elif node_type == "ScaleOperation":
                connector = "└── " if is_last else "├── "
                out_file.write(f"{prefix}{connector}ScaleStatement\n")
                continuation = "    " if is_last else "│   "
                out_file.write(f"{prefix}{continuation}├── Ingredient (Identifier): {node.ingredient}\n")
                out_file.write(f"{prefix}{continuation}└── Factor (Literal): {node.factor}\n")
            
            elif node_type == "AddOperation":
                connector = "└── " if is_last else "├── "
                out_file.write(f"{prefix}{connector}AddStatement\n")
                continuation = "    " if is_last else "│   "
                out_file.write(f"{prefix}{continuation}├── Ingredient (Identifier): {node.ingredient}\n")
                out_file.write(f"{prefix}{continuation}└── Target (Identifier): {node.target}\n")
            
            elif node_type == "RecipeCall":
                connector = "└── " if is_last else "├── "
                out_file.write(f"{prefix}{connector}RecipeCall\n")
                continuation = "    " if is_last else "│   "
                out_file.write(f"{prefix}{continuation}├── Name: {node.name}\n")
                out_file.write(f"{prefix}{continuation}└── Arguments (ExpressionList: {len(node.arguments)})\n")
                for i, arg in enumerate(node.arguments):
                    arg_is_last = (i == len(node.arguments) - 1)
                    arg_connector = "└── " if arg_is_last else "├── "
                    out_file.write(f"{prefix}{continuation}    {arg_connector}Expression: ")
                    print_ast_value(arg, out_file)
                    out_file.write("\n")
            
            elif node_type == "ReturnStatement":
                connector = "└── " if is_last else "├── "
                out_file.write(f"{prefix}{connector}ReturnStatement\n")
                continuation = "    " if is_last else "│   "
                if node.value:
                    out_file.write(f"{prefix}{continuation}└── Value (Expression): ")
                    print_ast_value(node.value, out_file)
                    out_file.write("\n")
                else:
                    out_file.write(f"{prefix}{continuation}└── Value: None\n")
            
            else:
                out_file.write(f"{indent_str}{prefix}{node_type}\n")
        
        def print_ast_value(node, out_file):
            """Print expression node inline with proper type annotations"""
            node_type = type(node).__name__
            if node_type == "Number":
                out_file.write(f"Literal({node.value})")
            elif node_type == "Identifier":
                out_file.write(f"Identifier({node.name})")
            elif node_type == "BinaryOp":
                op_str = str(node.op).split('.')[-1]
                out_file.write(f"BinaryExpression({op_str}, ")
                print_ast_value(node.left, out_file)
                out_file.write(", ")
                print_ast_value(node.right, out_file)
                out_file.write(")")
            elif node_type == "Value":
                out_file.write(f"ValueWithUnit(")
                if hasattr(node.number, '__class__') and type(node.number).__name__ in ['BinaryOp', 'Number', 'Identifier']:
                    print_ast_value(node.number, out_file)
                else:
                    out_file.write(str(node.number))
                if node.unit:
                    unit_str = str(node.unit).split('.')[-1].lower()
                    out_file.write(f", unit={unit_str}")
                out_file.write(")")
            elif node_type == "RecipeCall":
                out_file.write(f"RecipeCall({node.name})")
            else:
                out_file.write(f"{node_type}Node")
        
        print_ast_node(ast)
        
        # PHASE 3: SEMANTIC ANALYSIS
        out.write("\n" + "=" * 80 + "\n")
        out.write("PHASE 3: SEMANTIC ANALYSIS\n")
        out.write("=" * 80 + "\n\n")
        
        semantic_analyzer = SemanticAnalyzer()
        symbol_table = semantic_analyzer.analyze(ast)
        
        out.write("Symbol Table:\n")
        out.write("-" * 80 + "\n")
        out.write(f"{'Name':<20} {'Type':<15} {'Scope':<8} {'Line':<10} {'Context':<20}\n")
        out.write("-" * 80 + "\n")
        
        # Sort by scope first, then by line
        sorted_symbols = sorted(symbol_table.symbols.items(), key=lambda x: (x[1]['scope'], x[1]['line']))
        
        for name, info in sorted_symbols:
            type_str = str(info['type']).split('.')[-1] if hasattr(info['type'], 'name') else str(info['type'])
            display_name = info.get('original_name', name)
            
            # Determine context
            if info['scope'] == 0:
                if type_str == 'RECIPE':
                    context = "(function)"
                else:
                    context = "(global)"
            else:
                # For scope 1, check if it's marked as a parameter
                if info.get('is_parameter', False):
                    context = "(parameter)"
                else:
                    context = "(local)"
            
            out.write(f"{display_name:<20} {type_str:<15} {info['scope']:<8} {info['line']:<10} {context:<20}\n")
        
        out.write(f"\nTotal Symbols: {len(symbol_table.symbols)}\n")
        out.write("Semantic Analysis: PASSED\n")
        
        # PHASE 4: INTERMEDIATE CODE GENERATION
        out.write("\n" + "=" * 80 + "\n")
        out.write("PHASE 4: INTERMEDIATE CODE GENERATION (TAC)\n")
        out.write("=" * 80 + "\n\n")
        
        out.write("TAC Conventions:\n")
        out.write("  - Units: Treated as value attributes (e.g., '2 minutes', '350 fahrenheit')\n")
        out.write("  - Calls: Format 'result = CALL function, arg_count'\n")
        out.write("  - Loops: Exit condition using '>=' with 'if_true' (makes exit explicit)\n\n")
        
        ic_generator = IntermediateCodeGenerator()
        tac_instructions = ic_generator.generate(ast)
        
        out.write(f"Total TAC Instructions: {len(tac_instructions)}\n\n")
        out.write("Three-Address Code:\n")
        out.write("-" * 80 + "\n")
        for i, instr in enumerate(tac_instructions, 1):
            out.write(f"{i:4}: {instr}\n")
        
        # PHASE 5: CODE OPTIMIZATION
        out.write("\n" + "=" * 80 + "\n")
        out.write("PHASE 5: CODE OPTIMIZATION\n")
        out.write("=" * 80 + "\n\n")
        
        optimizer = Optimizer()
        optimized_instructions = optimizer.optimize(tac_instructions)
        
        out.write(f"Original Instructions: {len(tac_instructions)}\n")
        out.write(f"Optimized Instructions: {len(optimized_instructions)}\n")
        out.write(f"Instructions Removed: {len(tac_instructions) - len(optimized_instructions)}\n\n")
        
        if optimizer.optimizations_applied:
            out.write("Optimizations Applied:\n")
            out.write("-" * 80 + "\n")
            for opt in optimizer.optimizations_applied:
                out.write(f"  - {opt}\n")
        else:
            out.write("No optimizations applied (preserving correctness)\n")
        
        out.write("\nOptimized Three-Address Code:\n")
        out.write("-" * 80 + "\n")
        for i, instr in enumerate(optimized_instructions, 1):
            out.write(f"{i:4}: {instr}\n")
        
        # PHASE 6: CODE EXECUTION
        out.write("\n" + "=" * 80 + "\n")
        out.write("PHASE 6: CODE EXECUTION (RUNTIME)\n")
        out.write("=" * 80 + "\n\n")
        
        # Simulate input
        import io
        old_input = __builtins__.input
        __builtins__.input = lambda prompt: input_value
        
        code_generator = CodeGenerator()
        
        # Capture execution output
        out.write(f"Input: people = {input_value}\n\n")
        out.write("Execution Output:\n")
        out.write("-" * 80 + "\n")
        
        # Execute and capture output
        import sys
        from io import StringIO
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        try:
            code_generator.execute(optimized_instructions)
            execution_output = sys.stdout.getvalue()
        finally:
            sys.stdout = old_stdout
            __builtins__.input = old_input
        
        out.write(execution_output)
        
        # PHASE 7: ASSEMBLY CODE (Conceptual)
        out.write("\n" + "=" * 80 + "\n")
        out.write("PHASE 7: ASSEMBLY CODE (CONCEPTUAL)\n")
        out.write("=" * 80 + "\n\n")
        
        out.write("Note: RecipeScript is interpreted, not compiled to assembly.\n")
        out.write("Below is a conceptual representation of how TAC could map to assembly.\n\n")
        
        out.write("Conceptual Assembly Mapping:\n")
        out.write("-" * 80 + "\n")
        out.write("; Recipe: calculate_baking_time\n")
        out.write("calculate_baking_time:\n")
        out.write("    PUSH BP              ; Save base pointer\n")
        out.write("    MOV BP, SP           ; Set up stack frame\n")
        out.write("    MOV [base_time], 12  ; base_time = 12\n")
        out.write("    MOV AX, [pizzas]     ; Load pizzas\n")
        out.write("    MOV BX, 2            ; Divisor\n")
        out.write("    DIV BX               ; pizzas / 2\n")
        out.write("    MOV [extra_time], AX ; Store result\n")
        out.write("    ; ... (additional operations)\n")
        out.write("    MOV AX, [result]     ; Load return value\n")
        out.write("    POP BP               ; Restore base pointer\n")
        out.write("    RET                  ; Return\n\n")
        
        out.write("; Main program\n")
        out.write("main:\n")
        out.write("    CALL input_people    ; Get user input\n")
        out.write("    MOV AX, [people]     ; Load people count\n")
        out.write("    MOV BX, 2            ; Divisor\n")
        out.write("    DIV BX               ; people / 2\n")
        out.write("    MOV [pizzas], AX     ; Store pizzas\n")
        out.write("    ; ... (ingredient calculations)\n")
        out.write("    PUSH [pizzas]        ; Push arguments\n")
        out.write("    PUSH [oven_value]\n")
        out.write("    CALL calculate_baking_time\n")
        out.write("    ADD SP, 4            ; Clean up stack\n")
        out.write("    MOV [baking_time], AX\n")
        out.write("    CALL display_output  ; Show results\n")
        out.write("    HLT                  ; End program\n")
        
        # SUMMARY
        out.write("\n" + "=" * 80 + "\n")
        out.write("COMPILATION SUMMARY\n")
        out.write("=" * 80 + "\n\n")
        
        out.write(f"Source Lines: {len(source_code.splitlines())}\n")
        out.write(f"Tokens: {len(tokens)}\n")
        out.write(f"Recipes: {len(ast.recipes)}\n")
        out.write(f"Variables: {len(symbol_table.symbols)}\n")
        out.write(f"TAC Instructions: {len(tac_instructions)}\n")
        out.write(f"Optimized Instructions: {len(optimized_instructions)}\n")
        out.write(f"\nCompilation Status: SUCCESS\n")
        out.write(f"Execution Status: COMPLETED\n")
        
        out.write("\n" + "=" * 80 + "\n")
        out.write("END OF COMPILATION REPORT\n")
        out.write("=" * 80 + "\n")

if __name__ == "__main__":
    import sys
    
    # Allow command line argument for source file
    if len(sys.argv) > 1:
        source_file = sys.argv[1]
        output_file = "COMPILATION_REPORT_SHORT.txt" if "short" in source_file else "COMPILATION_REPORT.txt"
        input_val = "6" if "short" in source_file else "12"
    else:
        source_file = "examples/short_example.recipe"
        output_file = "COMPILATION_REPORT_SHORT.txt"
        input_val = "6"
    
    print(f"Generating compilation report for {source_file}...")
    generate_report(source_file, output_file, input_value=input_val)
    print(f"Report generated: {output_file}")
