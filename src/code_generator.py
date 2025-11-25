"""
Code Generator / Interpreter for RecipeScript
Phase 6: Executes Three-Address Code
"""

class CodeGenerator:
    def __init__(self):
        self.variables = {}
        self.output = []
        self.pc = 0  # Program counter
        self.labels = {}  # Label positions
    
    def execute(self, instructions):
        """Execute TAC instructions"""
        # First pass: collect label positions
        for i, instr in enumerate(instructions):
            if instr.op == 'label':
                self.labels[instr.result] = i
        
        # Second pass: execute instructions
        self.pc = 0
        while self.pc < len(instructions):
            instr = instructions[self.pc]
            self.execute_instruction(instr)
            self.pc += 1
        
        return self.output
    
    def execute_instruction(self, instr):
        """Execute single TAC instruction"""
        if instr.op == 'assign':
            value = self.get_value(instr.arg1)
            self.variables[instr.result] = value
        
        elif instr.op == 'add':
            val1 = self.get_value(instr.arg1)
            val2 = self.get_value(instr.arg2)
            self.variables[instr.result] = val1 + val2
        
        elif instr.op == 'sub':
            val1 = self.get_value(instr.arg1)
            val2 = self.get_value(instr.arg2)
            self.variables[instr.result] = val1 - val2
        
        elif instr.op == 'mul':
            val1 = self.get_value(instr.arg1)
            val2 = self.get_value(instr.arg2)
            self.variables[instr.result] = val1 * val2
        
        elif instr.op == 'div':
            val1 = self.get_value(instr.arg1)
            val2 = self.get_value(instr.arg2)
            if val2 == 0:
                raise Exception("Runtime Error: Division by zero")
            self.variables[instr.result] = val1 / val2
        
        elif instr.op == 'eq':
            val1 = self.get_value(instr.arg1)
            val2 = self.get_value(instr.arg2)
            self.variables[instr.result] = 1 if val1 == val2 else 0
        
        elif instr.op == 'neq':
            val1 = self.get_value(instr.arg1)
            val2 = self.get_value(instr.arg2)
            self.variables[instr.result] = 1 if val1 != val2 else 0
        
        elif instr.op == 'gt':
            val1 = self.get_value(instr.arg1)
            val2 = self.get_value(instr.arg2)
            self.variables[instr.result] = 1 if val1 > val2 else 0
        
        elif instr.op == 'lt':
            val1 = self.get_value(instr.arg1)
            val2 = self.get_value(instr.arg2)
            self.variables[instr.result] = 1 if val1 < val2 else 0
        
        elif instr.op == 'gte':
            val1 = self.get_value(instr.arg1)
            val2 = self.get_value(instr.arg2)
            self.variables[instr.result] = 1 if val1 >= val2 else 0
        
        elif instr.op == 'lte':
            val1 = self.get_value(instr.arg1)
            val2 = self.get_value(instr.arg2)
            self.variables[instr.result] = 1 if val1 <= val2 else 0
        
        elif instr.op == 'label':
            pass  # Labels are handled in first pass
        
        elif instr.op == 'goto':
            if instr.result in self.labels:
                self.pc = self.labels[instr.result] - 1  # -1 because pc will be incremented
            else:
                raise Exception(f"Runtime Error: Label {instr.result} not found")
        
        elif instr.op == 'if_false':
            condition = self.get_value(instr.arg1)
            if not condition or condition == 0:
                if instr.result in self.labels:
                    self.pc = self.labels[instr.result] - 1
                else:
                    raise Exception(f"Runtime Error: Label {instr.result} not found")
        
        elif instr.op == 'if_true':
            condition = self.get_value(instr.arg1)
            if condition and condition != 0:
                if instr.result in self.labels:
                    self.pc = self.labels[instr.result] - 1
                else:
                    raise Exception(f"Runtime Error: Label {instr.result} not found")
        
        elif instr.op == 'print':
            value = self.get_value(instr.arg1)
            self.output.append(str(value))
            print(value)
        
        elif instr.op == 'mix':
            ingredients = ', '.join(instr.arg1)
            msg = f"Mixing: {ingredients}"
            self.output.append(msg)
            print(msg)
        
        elif instr.op == 'heat':
            msg = f"Heating {instr.arg1} to {instr.arg2}"
            self.output.append(msg)
            print(msg)
        
        elif instr.op == 'wait':
            msg = f"Waiting for {instr.arg1}"
            self.output.append(msg)
            print(msg)
        
        elif instr.op == 'serve':
            msg = instr.arg1
            self.output.append(msg)
            print(msg)
        
        elif instr.op == 'scale':
            msg = f"Scaling {instr.arg1} by {instr.arg2}"
            self.output.append(msg)
            print(msg)
            # Update variable value
            if instr.arg1 in self.variables:
                current_val = self.variables[instr.arg1]
                # Extract numeric value if it's a string with units
                if isinstance(current_val, str):
                    parts = current_val.split()
                    if len(parts) >= 1:
                        try:
                            num_val = float(parts[0])
                            scale_factor = float(instr.arg2)
                            new_val = num_val * scale_factor
                            # Keep the unit if present
                            if len(parts) > 1:
                                self.variables[instr.arg1] = f"{new_val} {parts[1]}"
                            else:
                                self.variables[instr.arg1] = new_val
                        except ValueError:
                            pass
                else:
                    scale_factor = float(instr.arg2)
                    self.variables[instr.arg1] = current_val * scale_factor
        
        elif instr.op == 'add_ingredient':
            msg = f"Adding {instr.arg1} to {instr.arg2}"
            self.output.append(msg)
            print(msg)
    
    def get_value(self, operand):
        """Get value of operand (variable or constant)"""
        if operand is None:
            return None
        
        operand_str = str(operand)
        
        # Remove quotes from strings
        if operand_str.startswith('"') and operand_str.endswith('"'):
            return operand_str[1:-1]
        
        # Check if it's a number
        try:
            if '.' in operand_str:
                return float(operand_str)
            return int(operand_str)
        except ValueError:
            pass
        
        # Check if it's a variable
        if operand_str in self.variables:
            return self.variables[operand_str]
        
        # Return as string (for units, etc.)
        return operand_str
    
    def display_output(self):
        """Display program output"""
        print("\n" + "=" * 60)
        print("RECIPE EXECUTION OUTPUT")
        print("=" * 60)
        for line in self.output:
            print(line)
        print("=" * 60)
