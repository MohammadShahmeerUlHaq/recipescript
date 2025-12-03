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
        self.current_recipe = None
    
    def declare(self, name, var_type, line=0, is_parameter=False, recipe_name=None):
        """Declare a new variable"""
        # For recipe parameters and local variables, include recipe name in qualified name
        if self.scope_level > 0 and recipe_name:
            qualified_name = f"{name}_recipe_{recipe_name}"
        elif self.scope_level > 0:
            qualified_name = f"{name}_scope{self.scope_level}"
        else:
            qualified_name = name
        
        # Check if variable already exists with same qualified name
        if qualified_name in self.symbols:
            raise Exception(f"Semantic Error at line {line}: Variable '{name}' already declared in current scope")
        
        # Store with qualified name to allow same name in different scopes
        self.symbols[qualified_name] = {
            'type': var_type,
            'scope': self.scope_level,
            'line': line,
            'original_name': name,
            'is_parameter': is_parameter,
            'recipe_name': recipe_name
        }
    
    def lookup(self, name, line=0):
        """Look up a variable - search from current scope outward"""
        # If in a recipe scope, try recipe-qualified name first
        if self.scope_level > 0 and self.current_recipe:
            qualified_name = f"{name}_recipe_{self.current_recipe}"
            if qualified_name in self.symbols:
                return self.symbols[qualified_name]
        
        # Try current scope
        qualified_name = f"{name}_scope{self.scope_level}" if self.scope_level > 0 else name
        if qualified_name in self.symbols:
            return self.symbols[qualified_name]
        
        # Try outer scopes (search from current scope down to 0)
        for scope in range(self.scope_level - 1, -1, -1):
            qualified_name = f"{name}_scope{scope}" if scope > 0 else name
            if qualified_name in self.symbols:
                return self.symbols[qualified_name]
        
        # Not found in any scope
        raise Exception(f"Semantic Error at line {line}: Variable '{name}' not declared")

    
    def enter_scope(self):
        """Enter a new scope"""
        self.scope_level += 1
    
    def exit_scope(self):
        """Exit current scope"""
        # DON'T remove variables - keep them to show scope information
        # Just decrement scope level
        self.scope_level -= 1
    
    def display(self):
        """Display symbol table with proper formatting"""
        print("\n=== Symbol Table ===")
        print(f"{'Name':<20} {'Type':<15} {'Scope':<8} {'Line':<10} {'Context':<20}")
        print("-" * 75)
        
        # Sort by scope first, then by line
        sorted_symbols = sorted(self.symbols.items(), key=lambda x: (x[1]['scope'], x[1]['line']))
        
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
            
            print(f"{display_name:<20} {type_str:<15} {info['scope']:<8} {info['line']:<10} {context:<20}")

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.recipe_table = {}  # Store recipe definitions
        self.current_recipe = None  # Track current recipe being analyzed
        self.errors = []
        # Share current_recipe with symbol table for lookups
        self.symbol_table.current_recipe = None
    
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
        # First pass: Register all recipes (just names, not bodies)
        for recipe in node.recipes:
            self.register_recipe(recipe)
        
        # Second pass: Analyze main statements (declare global variables)
        for stmt in node.statements:
            self.visit(stmt)
        
        # Third pass: Analyze recipe bodies (now globals are declared)
        for recipe in node.recipes:
            self.visit(recipe)
    
    def visit_InputStatement(self, node):
        """Visit input statement"""
        # Declare input variable as quantity type
        line = getattr(node, 'line', 0)
        self.symbol_table.declare(node.var_name, TokenType.QUANTITY, line)
    
    def visit_Declaration(self, node):
        """Visit declaration node"""
        # Declare variable in symbol table
        line = getattr(node, 'line', 0)
        self.symbol_table.declare(node.name, node.var_type, line)
        
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
        
        # Visit then body (create new scope)
        self.symbol_table.enter_scope()
        for stmt in node.then_body:
            self.visit(stmt)
        # Exit scope (but variables are kept in symbol table)
        self.symbol_table.exit_scope()
        
        # Visit else body if exists (create new scope)
        if node.else_body:
            self.symbol_table.enter_scope()
            for stmt in node.else_body:
                self.visit(stmt)
            # Exit scope (but variables are kept in symbol table)
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
        
        # Add recipe to symbol table as a function
        line = getattr(recipe, 'line', 0)
        self.symbol_table.declare(recipe.name, 'RECIPE', line)
        
        self.recipe_table[recipe.name] = {
            'params': recipe.params,
            'return_type': recipe.return_type,
            'body': recipe.body,
            'line': line
        }
    
    def visit_RecipeDeclaration(self, node):
        """Visit recipe declaration"""
        self.current_recipe = node.name
        self.symbol_table.current_recipe = node.name
        
        # Create new scope for recipe
        self.symbol_table.enter_scope()
        
        # Add parameters to symbol table with recipe name
        line = getattr(node, 'line', 0)
        for param in node.params:
            self.symbol_table.declare(param['name'], param['type'], line, is_parameter=True, recipe_name=node.name)
        
        # Analyze recipe body
        has_return = False
        for stmt in node.body:
            self.visit(stmt)
            if isinstance(stmt, ReturnStatement):
                has_return = True
        
        # Check if recipe with return type has return statement
        if node.return_type and not has_return:
            self.error(f"Recipe '{node.name}' must return a value")
        
        # Exit recipe scope (but variables are kept in symbol table)
        self.symbol_table.exit_scope()
        self.current_recipe = None
        self.symbol_table.current_recipe = None
    
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
