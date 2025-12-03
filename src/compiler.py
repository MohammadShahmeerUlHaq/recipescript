"""
RecipeScript Compiler - Main Entry Point
Demonstrates all 6 phases of compilation
"""

import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lexer import Lexer
from parser import Parser
from semantic_analyzer import SemanticAnalyzer
from intermediate_code import IntermediateCodeGenerator
from optimizer import Optimizer
from code_generator import CodeGenerator

def print_separator(title):
    """Print section separator"""
    print("\n" + "=" * 60)
    print(f"PHASE {title}")
    print("=" * 60)

def compile_and_run(source_code, show_phases=True):
    """Compile and execute RecipeScript code"""
    try:
        # Phase 1: Lexical Analysis
        if show_phases:
            print_separator("1: LEXICAL ANALYSIS")
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        if show_phases:
            print(f"Generated {len(tokens)} tokens:")
            for token in tokens[:20]:  # Show first 20 tokens
                print(f"  {token}")
            if len(tokens) > 20:
                print(f"  ... and {len(tokens) - 20} more tokens")
        
        # Phase 2: Syntax Analysis
        if show_phases:
            print_separator("2: SYNTAX ANALYSIS")
        parser = Parser(tokens)
        ast = parser.parse()
        if show_phases:
            print(f"Successfully parsed {len(ast.recipes)} recipes and {len(ast.statements)} statements")
            print("Abstract Syntax Tree (AST) built successfully")
        
        # Phase 3: Semantic Analysis
        if show_phases:
            print_separator("3: SEMANTIC ANALYSIS")
        semantic_analyzer = SemanticAnalyzer()
        symbol_table = semantic_analyzer.analyze(ast)
        if show_phases:
            symbol_table.display()
            print("\nSemantic analysis completed successfully")
        
        # Phase 4: Intermediate Code Generation
        if show_phases:
            print_separator("4: INTERMEDIATE CODE GENERATION")
        ic_generator = IntermediateCodeGenerator()
        tac_instructions = ic_generator.generate(ast)
        if show_phases:
            ic_generator.display()
        
        # Phase 5: Code Optimization
        if show_phases:
            print_separator("5: CODE OPTIMIZATION")
        optimizer = Optimizer()
        optimized_instructions = optimizer.optimize(tac_instructions)
        if show_phases:
            print("\n=== Optimized Code ===")
            for i, instr in enumerate(optimized_instructions, 1):
                print(f"{i:3}: {instr}")
            optimizer.display_optimizations()
        
        # Phase 6: Code Generation / Execution
        if show_phases:
            print_separator("6: CODE EXECUTION")
        code_generator = CodeGenerator()
        output = code_generator.execute(optimized_instructions)
        
        if show_phases:
            print("\nExecution completed successfully!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

def run_file(filename):
    """Compile and run a RecipeScript file"""
    try:
        with open(filename, 'r') as f:
            source_code = f.read()
        
        print(f"\n{'=' * 60}")
        print(f"Compiling: {filename}")
        print(f"{'=' * 60}")
        
        success = compile_and_run(source_code, show_phases=True)
        
        if success:
            print(f"\n[SUCCESS] Successfully compiled and executed {filename}")
        else:
            print(f"\n[FAILED] Failed to compile {filename}")
        
        return success
        
    except FileNotFoundError:
        print(f"[ERROR] File '{filename}' not found")
        return False
    except Exception as e:
        print(f"[ERROR] Error reading file: {e}")
        return False

def interactive_mode():
    """Interactive REPL mode"""
    print("=" * 60)
    print("RecipeScript Interactive Mode")
    print("=" * 60)
    print("Enter RecipeScript code (type 'exit' to quit)")
    print("Type 'help' for examples")
    print("=" * 60)
    
    while True:
        try:
            line = input("\n>>> ")
            
            if line.strip().lower() == 'exit':
                print("Goodbye!")
                break
            
            if line.strip().lower() == 'help':
                print("\nExample commands:")
                print("  ingredient flour = 2 cups;")
                print("  temp oven = 350 F;")
                print("  heat oven to 350 F;")
                print("  wait 15 minutes;")
                print("  serve \"Ready!\";")
                continue
            
            if not line.strip():
                continue
            
            # Compile and run the line
            compile_and_run(line, show_phases=False)
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except EOFError:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

def main():
    """Main entry point"""
    print("=" * 60)
    print("RecipeScript Compiler")
    print("A Domain-Specific Language for Cooking Recipes")
    print("=" * 60)
    
    if len(sys.argv) > 1:
        # File mode
        filename = sys.argv[1]
        run_file(filename)
    else:
        # Interactive mode
        interactive_mode()

if __name__ == "__main__":
    main()
