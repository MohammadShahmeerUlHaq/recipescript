"""
Code Optimizer for RecipeScript
Phase 5: Optimizes Three-Address Code
"""

class Optimizer:
    def __init__(self):
        self.optimizations_applied = []
    
    def optimize(self, instructions):
        """Apply optimizations to TAC"""
        optimized = instructions.copy()
        
        # Apply constant folding
        optimized = self.constant_folding(optimized)
        
        # Apply dead code elimination
        optimized = self.dead_code_elimination(optimized)
        
        return optimized
    
    def constant_folding(self, instructions):
        """Fold constant expressions"""
        # Disable constant folding for now to avoid breaking loops
        # This is a simple implementation that needs more sophisticated analysis
        return instructions
    
    def dead_code_elimination(self, instructions):
        """Remove dead code (unused assignments)"""
        # Disable dead code elimination for now to avoid breaking loops
        # This needs more sophisticated analysis to handle control flow
        return instructions
    
    def is_constant(self, value):
        """Check if value is a constant"""
        if value is None:
            return False
        value_str = str(value)
        # Check if it's a number (int or float)
        try:
            float(value_str)
            return True
        except ValueError:
            return False
    
    def evaluate_op(self, op, arg1, arg2):
        """Evaluate arithmetic operation"""
        val1 = float(arg1)
        val2 = float(arg2)
        
        if op == 'add':
            return val1 + val2
        elif op == 'sub':
            return val1 - val2
        elif op == 'mul':
            return val1 * val2
        elif op == 'div':
            if val2 == 0:
                raise Exception("Division by zero in constant folding")
            return val1 / val2
        
        return 0
    
    def evaluate_comparison(self, op, arg1, arg2):
        """Evaluate comparison operation"""
        val1 = float(arg1)
        val2 = float(arg2)
        
        if op == 'eq':
            return 1 if val1 == val2 else 0
        elif op == 'neq':
            return 1 if val1 != val2 else 0
        elif op == 'gt':
            return 1 if val1 > val2 else 0
        elif op == 'lt':
            return 1 if val1 < val2 else 0
        elif op == 'gte':
            return 1 if val1 >= val2 else 0
        elif op == 'lte':
            return 1 if val1 <= val2 else 0
        
        return 0
    
    def display_optimizations(self):
        """Display applied optimizations"""
        if self.optimizations_applied:
            print("\n=== Optimizations Applied ===")
            for opt in self.optimizations_applied:
                print(f"  - {opt}")
        else:
            print("\n=== No Optimizations Applied ===")
