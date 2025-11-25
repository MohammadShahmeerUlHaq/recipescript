"""
Intermediate Code Generator for RecipeScript
Phase 4: Generates Three-Address Code (TAC)
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
        elif self.op == 'scale':
            return f"scale {self.arg1} by {self.arg2}"
        elif self.op == 'add_ingredient':
            return f"add {self.arg1} to {self.arg2}"
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
        for stmt in node.statements:
            self.visit(stmt)
    
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
    
    def visit_ScaleOperation(self, node):
        """Visit scale operation"""
        self.emit('scale', node.ingredient, node.factor)
    
    def visit_AddOperation(self, node):
        """Visit add operation"""
        self.emit('add_ingredient', node.ingredient, node.target)
    
    def visit_RepeatStatement(self, node):
        """Visit repeat statement"""
        # Generate loop structure
        # counter = 0
        # L1: if counter >= count goto L2
        # body
        # counter = counter + 1
        # goto L1
        # L2:
        
        counter = self.new_temp()
        label_start = self.new_label()
        label_end = self.new_label()
        
        self.emit('assign', '0', None, counter)
        self.emit('label', None, None, label_start)
        
        # Check condition (if counter >= count, exit loop)
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
        """Visit value node"""
        if node.unit:
            unit_str = str(node.unit).split('.')[-1].lower()
            return f"{node.number} {unit_str}"
        return node.number
    
    def display(self):
        """Display generated TAC"""
        print("\n=== Three-Address Code ===")
        for i, instr in enumerate(self.instructions, 1):
            print(f"{i:3}: {instr}")
