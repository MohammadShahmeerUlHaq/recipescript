"""
Intermediate Code Generator for RecipeScript
Phase 4: Generates Three-Address Code (TAC)

TAC Conventions Used:
---------------------
1. UNITS: Units are treated as value attributes (domain-specific for cooking)
   Format: "value unit" (e.g., "2 minutes", "350 fahrenheit")
   Example: t0 = 2 minutes
   
2. FUNCTION CALLS: Standard format with argument count
   Format: result = CALL function_name, arg_count
   Example: t10 = CALL make_dough, 2
   
3. LOOP CONDITIONS: Exit condition using >= with if_true
   Format: if counter >= limit goto exit_label
   Note: Equivalent to "if counter < limit goto continue" but makes exit explicit
   
4. LABELS: Sequential numbering (L0, L1, L2, ...)
   
5. TEMPORARIES: Sequential numbering (t0, t1, t2, ...)
   
6. OPERATIONS: Standard arithmetic (add, sub, mul, div) and comparisons (eq, neq, gt, lt, gte, lte)
"""

from parser import *
from token_types import TokenType

class TACInstruction:
    """Three-Address Code instruction"""
    def __init__(self, op, arg1=None, arg2=None, result=None):
        self.op = op
        self.arg1 = arg1
        self.arg2 = arg2
        self.result = result
    
    def __str__(self):
        if self.op == 'assign':
            return f"{self.result} = {self.arg1}"
        elif self.op in ['add', 'sub', 'mul', 'div']:
            op_symbol = {
                'add': '+', 'sub': '-', 'mul': '*', 'div': '/'
            }[self.op]
            return f"{self.result} = {self.arg1} {op_symbol} {self.arg2}"
        elif self.op in ['eq', 'neq', 'gt', 'lt', 'gte', 'lte']:
            op_symbol = {
                'eq': '==', 'neq': '!=', 'gt': '>', 
                'lt': '<', 'gte': '>=', 'lte': '<='
            }[self.op]
            return f"{self.result} = {self.arg1} {op_symbol} {self.arg2}"
        elif self.op == 'label':
            return f"{self.result}:"
        elif self.op == 'goto':
            return f"goto {self.result}"
        elif self.op == 'if_false':
            return f"if_false {self.arg1} goto {self.result}"
        elif self.op == 'if_true':
            return f"if_true {self.arg1} goto {self.result}"
        elif self.op == 'print':
            return f"print {self.arg1}"
        elif self.op == 'mix':
            ingredients = ', '.join(self.arg1)
            return f"mix {ingredients}"
        elif self.op == 'heat':
            return f"heat {self.arg1} to {self.arg2}"
        elif self.op == 'wait':
            return f"wait {self.arg1}"
        elif self.op == 'serve':
            return f"serve \"{self.arg1}\""
        elif self.op == 'display':
            return f"display {self.arg1}"
        elif self.op == 'scale':
            return f"scale {self.arg1} by {self.arg2}"
        elif self.op == 'add_ingredient':
            return f"add {self.arg1} to {self.arg2}"
        elif self.op == 'input':
            return f"input {self.result}"
        elif self.op == 'begin_recipe':
            return f"RECIPE {self.result}:"
        elif self.op == 'end_recipe':
            return f"END_RECIPE {self.result}"
        elif self.op == 'param':
            return f"PARAM {self.arg1}"
        elif self.op == 'call':
            return f"{self.result} = CALL {self.arg1}, {self.arg2}"
        elif self.op == 'return':
            if self.arg1:
                return f"RETURN {self.arg1}"
            return "RETURN"
        else:
            return f"{self.op} {self.arg1} {self.arg2} {self.result}"

class IntermediateCodeGenerator:
    def __init__(self):
        self.instructions = []
        self.temp_counter = 0
        self.label_counter = 0
    
    def new_temp(self):
        """Generate new temporary variable"""
        temp = f"t{self.temp_counter}"
        self.temp_counter += 1
        return temp
    
    def new_label(self):
        """Generate new label"""
        label = f"L{self.label_counter}"
        self.label_counter += 1
        return label
    
    def emit(self, op, arg1=None, arg2=None, result=None):
        """Emit a TAC instruction"""
        instr = TACInstruction(op, arg1, arg2, result)
        self.instructions.append(instr)
        return instr
    
    def generate(self, ast):
        """Generate TAC for AST"""
        self.visit(ast)
        return self.instructions
    
    def visit(self, node):
        """Visit AST node"""
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
    
    def generic_visit(self, node):
        """Default visitor"""
        return None
    
    def visit_Program(self, node):
        """Visit program node"""
        # Generate code for recipes first
        for recipe in node.recipes:
            self.visit(recipe)
        
        # Then generate code for main statements
        for stmt in node.statements:
            self.visit(stmt)
    
    def visit_InputStatement(self, node):
        """Visit input statement"""
        self.emit('input', None, None, node.var_name)
    
    def visit_Declaration(self, node):
        """Visit declaration node"""
        value = self.visit(node.value)
        self.emit('assign', value, None, node.name)
    
    def visit_Assignment(self, node):
        """Visit assignment node"""
        value = self.visit(node.value)
        self.emit('assign', value, None, node.name)
    
    def visit_MixOperation(self, node):
        """Visit mix operation"""
        self.emit('mix', node.ingredients)
    
    def visit_HeatOperation(self, node):
        """Visit heat operation"""
        temp_value = self.visit(node.temperature)
        self.emit('heat', node.target, temp_value)
    
    def visit_WaitOperation(self, node):
        """Visit wait operation"""
        duration = self.visit(node.duration)
        self.emit('wait', duration)
    
    def visit_ServeOperation(self, node):
        """Visit serve operation"""
        self.emit('serve', node.message)
    
    def visit_DisplayOperation(self, node):
        """Visit display operation"""
        self.emit('display', node.variable)
    
    def visit_ScaleOperation(self, node):
        """Visit scale operation"""
        self.emit('scale', node.ingredient, node.factor)
    
    def visit_AddOperation(self, node):
        """Visit add operation"""
        self.emit('add_ingredient', node.ingredient, node.target)
    
    def visit_RepeatStatement(self, node):
        """
        Visit repeat statement and generate loop TAC.
        
        Loop structure (using >= and if_true for exit condition):
            counter = 0
            L_start: 
                if counter >= count goto L_end    # Exit when done
                <body>
                counter = counter + 1
                goto L_start
            L_end:
        
        Note: We use "if counter >= count" with if_true instead of the more
        common "if counter < count" with if_false. Both are semantically
        equivalent, but this form makes the exit condition explicit.
        """
        counter = self.new_temp()
        label_start = self.new_label()
        label_end = self.new_label()
        
        # Initialize counter
        self.emit('assign', '0', None, counter)
        self.emit('label', None, None, label_start)
        
        # Check exit condition: if counter >= count, exit loop
        temp_cond = self.new_temp()
        self.emit('gte', counter, node.count, temp_cond)
        self.emit('if_true', temp_cond, None, label_end)
        
        # Body
        for stmt in node.body:
            self.visit(stmt)
        
        # Increment counter
        temp_inc = self.new_temp()
        self.emit('add', counter, '1', temp_inc)
        self.emit('assign', temp_inc, None, counter)
        
        self.emit('goto', None, None, label_start)
        self.emit('label', None, None, label_end)
    
    def visit_WhenStatement(self, node):
        """Visit when statement"""
        # Generate conditional structure
        # condition
        # if_false condition goto L1
        # then_body
        # goto L2
        # L1: else_body
        # L2:
        
        cond_result = self.visit(node.condition)
        label_else = self.new_label()
        label_end = self.new_label()
        
        self.emit('if_false', cond_result, None, label_else)
        
        # Then body
        for stmt in node.then_body:
            self.visit(stmt)
        
        self.emit('goto', None, None, label_end)
        self.emit('label', None, None, label_else)
        
        # Else body
        if node.else_body:
            for stmt in node.else_body:
                self.visit(stmt)
        
        self.emit('label', None, None, label_end)
    
    def visit_BinaryOp(self, node):
        """Visit binary operation"""
        left = self.visit(node.left)
        right = self.visit(node.right)
        result = self.new_temp()
        
        op_map = {
            TokenType.PLUS: 'add',
            TokenType.MINUS: 'sub',
            TokenType.MULTIPLY: 'mul',
            TokenType.DIVIDE: 'div',
            TokenType.EQ: 'eq',
            TokenType.NEQ: 'neq',
            TokenType.GT: 'gt',
            TokenType.LT: 'lt',
            TokenType.GTE: 'gte',
            TokenType.LTE: 'lte',
        }
        
        op = op_map.get(node.op, 'unknown')
        self.emit(op, left, right, result)
        return result
    
    def visit_Number(self, node):
        """Visit number node"""
        return node.value
    
    def visit_String(self, node):
        """Visit string node"""
        return f'"{node.value}"'
    
    def visit_Identifier(self, node):
        """Visit identifier node"""
        return node.name
    
    def visit_Value(self, node):
        """
        Visit value node (number with optional unit).
        Handles both simple values and complex expressions with units.
        
        Returns:
            str or number: The value, optionally formatted with its unit
        """
        # Check if number is an AST node (expression) or a simple value
        if hasattr(node.number, '__class__'):
            class_name = node.number.__class__.__name__
            if class_name in ['BinaryOp', 'Number', 'Identifier']:
                # It's an expression, visit it to get the result
                number_result = self.visit(node.number)
            else:
                # It's a simple string value
                number_result = node.number
        else:
            number_result = node.number
        
        # If there's a unit, create a value with unit annotation
        # In RecipeScript, units are domain-specific and treated as value attributes
        # TAC format: "value unit" (e.g., "2 minutes", "350 fahrenheit")
        # This is intentional for a cooking DSL where units are essential
        if node.unit:
            unit_str = str(node.unit).split('.')[-1].lower()
            # Create a temp to hold the value with unit
            temp = self.new_temp()
            self.emit('assign', f"{number_result} {unit_str}", None, temp)
            return temp
        return number_result
    
    def visit_RecipeDeclaration(self, node):
        """Visit recipe declaration"""
        self.emit('begin_recipe', None, None, node.name)
        
        # Generate code for body
        for stmt in node.body:
            self.visit(stmt)
        
        self.emit('end_recipe', None, None, node.name)
    
    def visit_RecipeCall(self, node):
        """Visit recipe call"""
        # Evaluate and push arguments
        for arg in node.arguments:
            arg_result = self.visit(arg)
            self.emit('param', arg_result)
        
        # Call recipe
        result = self.new_temp()
        self.emit('call', node.name, len(node.arguments), result)
        return result
    
    def visit_ReturnStatement(self, node):
        """Visit return statement"""
        if node.value:
            value = self.visit(node.value)
            self.emit('return', value)
        else:
            self.emit('return', None)
    
    def display(self):
        """Display generated TAC"""
        print("\n=== Three-Address Code ===")
        for i, instr in enumerate(self.instructions, 1):
            print(f"{i:3}: {instr}")
