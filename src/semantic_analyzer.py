"""
Semantic Analyzer for RecipeScript
Phase 3: Type checking and symbol table construction
"""

from token_types import TokenType
from parser import *

class SymbolTable:
    def __init__(self):
        self.symbols = {}
        self.scope_level = 0
    
    def declare(self, name, var_type, line=0):
        """Declare a new variable"""
        if name in self.symbols:
            raise Exception(f"Semantic Error at line {line}: Variable '{name}' already declared")
        self.symbols[name] = {
            'type': var_type,
            'scope': self.scope_level,
            'line': line
        }
    
    def lookup(self, name, line=0):
        """Look up a variable"""
        if name not in self.symbols:
            raise Exception(f"Semantic Error at line {line}: Variable '{name}' not declared")
        return self.symbols[name]
    
    def enter_scope(self):
        """Enter a new scope"""
        self.scope_level += 1
    
    def exit_scope(self):
        """Exit current scope"""
        # Remove variables from current scope
        self.symbols = {k: v for k, v in self.symbols.items() if v['scope'] < self.scope_level}
        self.scope_level -= 1
    
    def display(self):
        """Display symbol table"""
        print("\n=== Symbol Table ===")
        print(f"{'Name':<15} {'Type':<15} {'Scope':<8} {'Line':<8}")
        print("-" * 50)
        for name, info in self.symbols.items():
            type_str = str(info['type']).split('.')[-1] if hasattr(info['type'], 'name') else str(info['type'])
            print(f"{name:<15} {type_str:<15} {info['scope']:<8} {info['line']:<8}")

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.recipe_table = {}  # Store recipe definitions
        self.current_recipe = None  # Track current recipe being analyzed
        self.errors = []
    
    def error(self, msg):
        """Record semantic error"""
        self.errors.append(msg)
        raise Exception(f"Semantic Error: {msg}")
    
    def analyze(self, ast):
        """Analyze the AST"""
        self.visit(ast)
        return self.symbol_table
    
    def visit(self, node):
        """Visit AST node"""
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
    
    def generic_visit(self, node):
        """Default visitor"""
        pass
    
    def visit_Program(self, node):
        """Visit program node"""
        # First pass: Register all recipes
        for recipe in node.recipes:
            self.register_recipe(recipe)
        
        # Second pass: Analyze recipe bodies
        for recipe in node.recipes:
            self.visit(recipe)
        
        # Third pass: Analyze main statements
        for stmt in node.statements:
            self.visit(stmt)
    
    def visit_InputStatement(self, node):
        """Visit input statement"""
        # Declare input variable as quantity type
        self.symbol_table.declare(node.var_name, TokenType.QUANTITY)
    
    def visit_Declaration(self, node):
        """Visit declaration node"""
        # Declare variable in symbol table
        self.symbol_table.declare(node.name, node.var_type)
        
        # Check value type compatibility
        self.visit(node.value)
    
    def visit_Assignment(self, node):
        """Visit assignment node"""
        # Check if variable exists
        self.symbol_table.lookup(node.name)
        self.visit(node.value)
    
    def visit_MixOperation(self, node):
        """Visit mix operation"""
        # Check all ingredients are declared
        for ingredient in node.ingredients:
            var_info = self.symbol_table.lookup(ingredient)
            if var_info['type'] != TokenType.INGREDIENT:
                self.error(f"Cannot mix non-ingredient: {ingredient}")
    
    def visit_HeatOperation(self, node):
        """Visit heat operation"""
        # Check target exists
        self.symbol_table.lookup(node.target)
        self.visit(node.temperature)
        
        # Validate temperature range (only for constant values)
        if isinstance(node.temperature, Value):
            # Check if number is a simple value (not an expression)
            if isinstance(node.temperature.number, str):
                try:
                    temp_val = float(node.temperature.number)
                    if node.temperature.unit == TokenType.FAHRENHEIT:
                        if temp_val < 0 or temp_val > 500:
                            self.error(f"Temperature out of range: {temp_val}F (0-500F)")
                    elif node.temperature.unit == TokenType.CELSIUS:
                        if temp_val < 0 or temp_val > 260:
                            self.error(f"Temperature out of range: {temp_val}C (0-260C)")
                except ValueError:
                    pass  # Skip validation for non-numeric values
    
    def visit_WaitOperation(self, node):
        """Visit wait operation"""
        self.visit(node.duration)
        
        # Validate positive duration (only for constant values)
        if isinstance(node.duration, Value):
            if isinstance(node.duration.number, str):
                try:
                    duration_val = float(node.duration.number)
                    if duration_val < 0:
                        self.error(f"Duration must be positive: {duration_val}")
                except ValueError:
                    pass  # Skip validation for non-numeric values
    
    def visit_ServeOperation(self, node):
        """Visit serve operation"""
        pass  # No semantic checks needed
    
    def visit_DisplayOperation(self, node):
        """Visit display operation"""
        # Check variable exists
        self.symbol_table.lookup(node.variable)
    
    def visit_ScaleOperation(self, node):
        """Visit scale operation"""
        # Check ingredient exists
        var_info = self.symbol_table.lookup(node.ingredient)
        if var_info['type'] != TokenType.INGREDIENT:
            self.error(f"Cannot scale non-ingredient: {node.ingredient}")
        
        # Validate positive factor
        factor_val = float(node.factor)
        if factor_val <= 0:
            self.error(f"Scale factor must be positive: {factor_val}")
    
    def visit_AddOperation(self, node):
        """Visit add operation"""
        # Check both ingredients exist
        self.symbol_table.lookup(node.ingredient)
        self.symbol_table.lookup(node.target)
    
    def visit_RepeatStatement(self, node):
        """Visit repeat statement"""
        # Validate positive count
        count_val = int(node.count)
        if count_val <= 0:
            self.error(f"Repeat count must be positive: {count_val}")
        
        # Visit body statements
        self.symbol_table.enter_scope()
        for stmt in node.body:
            self.visit(stmt)
        self.symbol_table.exit_scope()
    
    def visit_WhenStatement(self, node):
        """Visit when statement"""
        # Visit condition
        self.visit(node.condition)
        
        # Visit then body
        self.symbol_table.enter_scope()
        for stmt in node.then_body:
            self.visit(stmt)
        self.symbol_table.exit_scope()
        
        # Visit else body if exists
        if node.else_body:
            self.symbol_table.enter_scope()
            for stmt in node.else_body:
                self.visit(stmt)
            self.symbol_table.exit_scope()
    
    def visit_BinaryOp(self, node):
        """Visit binary operation"""
        self.visit(node.left)
        self.visit(node.right)
    
    def visit_Number(self, node):
        """Visit number node"""
        pass
    
    def visit_String(self, node):
        """Visit string node"""
        pass
    
    def visit_Identifier(self, node):
        """Visit identifier node"""
        self.symbol_table.lookup(node.name)
    
    def visit_Value(self, node):
        """Visit value node"""
        pass
    
    def register_recipe(self, recipe):
        """Register recipe in recipe table"""
        if recipe.name in self.recipe_table:
            self.error(f"Recipe '{recipe.name}' already defined")
        
        self.recipe_table[recipe.name] = {
            'params': recipe.params,
            'return_type': recipe.return_type,
            'body': recipe.body
        }
    
    def visit_RecipeDeclaration(self, node):
        """Visit recipe declaration"""
        self.current_recipe = node.name
        
        # Create new scope for recipe
        self.symbol_table.enter_scope()
        
        # Add parameters to symbol table
        for param in node.params:
            self.symbol_table.declare(param['name'], param['type'])
        
        # Analyze recipe body
        has_return = False
        for stmt in node.body:
            self.visit(stmt)
            if isinstance(stmt, ReturnStatement):
                has_return = True
        
        # Check if recipe with return type has return statement
        if node.return_type and not has_return:
            self.error(f"Recipe '{node.name}' must return a value")
        
        # Exit recipe scope
        self.symbol_table.exit_scope()
        self.current_recipe = None
    
    def visit_RecipeCall(self, node):
        """Visit recipe call"""
        # Check if recipe exists
        if node.name not in self.recipe_table:
            self.error(f"Undefined recipe '{node.name}'")
            return
        
        recipe = self.recipe_table[node.name]
        
        # Check argument count
        expected = len(recipe['params'])
        actual = len(node.arguments)
        
        if expected != actual:
            self.error(
                f"Recipe '{node.name}' expects {expected} arguments, got {actual}"
            )
            return
        
        # Visit arguments
        for arg in node.arguments:
            self.visit(arg)
    
    def visit_ReturnStatement(self, node):
        """Visit return statement"""
        if not self.current_recipe:
            self.error("Return statement outside recipe")
        
        if node.value:
            self.visit(node.value)
