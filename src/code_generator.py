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
        self.recipes = {}  # Recipe definitions
        self.call_stack = []  # Function call stack
        self.param_stack = []  # Parameter stack
    
    def execute(self, instructions):
        """Execute TAC instructions"""
        # First pass: collect label positions and recipe definitions
        for i, instr in enumerate(instructions):
            if instr.op == 'label':
                self.labels[instr.result] = i
            elif instr.op == 'begin_recipe':
                self.recipes[instr.result] = i
        
        # Second pass: execute instructions (skip recipe bodies initially)
        self.pc = 0
        while self.pc < len(instructions):
            instr = instructions[self.pc]
            
            # Skip recipe definitions during main execution
            if instr.op == 'begin_recipe':
                # Find end of recipe
                depth = 1
                self.pc += 1
                while self.pc < len(instructions) and depth > 0:
                    if instructions[self.pc].op == 'begin_recipe':
                        depth += 1
                    elif instructions[self.pc].op == 'end_recipe':
                        depth -= 1
                    self.pc += 1
                continue
            
            result = self.execute_instruction(instr, instructions)
            if result == 'return':
                break
            self.pc += 1
        
        return self.output
    
    def execute_instruction(self, instr, instructions=None):
        """Execute single TAC instruction"""
        if instr.op == 'begin_recipe' or instr.op == 'end_recipe':
            return None
        
        elif instr.op == 'param':
            # Push parameter onto stack
            value = self.get_value(instr.arg1)
            self.param_stack.append(value)
        
        elif instr.op == 'call':
            # Call recipe
            recipe_name = instr.arg1
            arg_count = instr.arg2
            
            if recipe_name not in self.recipes:
                raise Exception(f"Runtime Error: Recipe '{recipe_name}' not defined")
            
            # Pop arguments from param stack
            args = []
            for _ in range(arg_count):
                if self.param_stack:
                    args.insert(0, self.param_stack.pop())
            
            # Execute recipe
            result = self.execute_recipe(recipe_name, args, instructions)
            self.variables[instr.result] = result
        
        elif instr.op == 'return':
            # Return from recipe
            if instr.arg1:
                return_value = self.get_value(instr.arg1)
                return ('return', return_value)
            return ('return', None)
        
        elif instr.op == 'assign':
            value = self.get_value(instr.arg1)
            # If assigning a temp variable value, resolve it
            if isinstance(value, str) and value.startswith('t') and value[1:].isdigit():
                # It's a temp variable reference, get its value
                if value in self.variables:
                    value = self.variables[value]
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
            duration = self.get_value(instr.arg1)
            msg = f"Waiting for {duration}"
            self.output.append(msg)
            print(msg)
        
        elif instr.op == 'serve':
            msg = instr.arg1
            self.output.append(msg)
            print(msg)
        
        elif instr.op == 'display':
            # Display variable name and value
            var_name = instr.arg1
            if var_name in self.variables:
                value = self.variables[var_name]
                # Resolve any temp variable references in the value
                if isinstance(value, str):
                    parts = value.split()
                    if len(parts) >= 2:
                        # Check if first part is a temp variable
                        if parts[0].startswith('t') and parts[0][1:].isdigit():
                            if parts[0] in self.variables:
                                resolved_val = self.variables[parts[0]]
                                value = f"{resolved_val} {' '.join(parts[1:])}"
                msg = f"{var_name}: {value}"
                self.output.append(msg)
                print(msg)
            else:
                msg = f"{var_name}: (not set)"
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
        
        elif instr.op == 'input':
            # Prompt user for input
            try:
                value = input(f"Enter value for {instr.result}: ")
                # Try to convert to number
                try:
                    if '.' in value:
                        self.variables[instr.result] = float(value)
                    else:
                        self.variables[instr.result] = int(value)
                except ValueError:
                    self.variables[instr.result] = value
            except EOFError:
                # For non-interactive mode, use default value
                self.variables[instr.result] = 4  # Default servings
    
    def execute_recipe(self, recipe_name, args, instructions):
        """Execute a recipe with given arguments"""
        # Save current state
        saved_pc = self.pc
        saved_vars = self.variables.copy()
        
        # Find recipe declaration to get parameter names
        # We need to parse the recipe to find parameter names
        # For now, we'll use a simple approach: pass args as local variables
        # In a full implementation, we'd need to track parameter names
        
        # Find recipe start
        recipe_start = self.recipes[recipe_name]
        self.pc = recipe_start + 1  # Skip begin_recipe instruction
        
        # Execute recipe body with arguments available
        # Store arguments in variables (they'll be referenced by name in the recipe)
        return_value = None
        while self.pc < len(instructions):
            instr = instructions[self.pc]
            
            if instr.op == 'end_recipe' and instr.result == recipe_name:
                break
            
            result = self.execute_instruction(instr, instructions)
            if result and isinstance(result, tuple) and result[0] == 'return':
                return_value = result[1]
                break
            
            self.pc += 1
        
        # Restore state
        self.pc = saved_pc
        # Keep only global variables, restore locals
        for key in list(self.variables.keys()):
            if key not in saved_vars:
                del self.variables[key]
        
        return return_value if return_value is not None else 0
    
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
