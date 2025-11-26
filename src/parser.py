"""
Syntax Analyzer (Parser) for RecipeScript
Phase 2: Builds Abstract Syntax Tree from tokens
"""

from token_types import TokenType

class ASTNode:
    """Base class for AST nodes"""
    pass

class Program(ASTNode):
    def __init__(self, statements):
        self.statements = statements

class Declaration(ASTNode):
    def __init__(self, var_type, name, value):
        self.var_type = var_type
        self.name = name
        self.value = value

class Assignment(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value

class MixOperation(ASTNode):
    def __init__(self, ingredients):
        self.ingredients = ingredients

class HeatOperation(ASTNode):
    def __init__(self, target, temperature):
        self.target = target
        self.temperature = temperature

class WaitOperation(ASTNode):
    def __init__(self, duration):
        self.duration = duration

class ServeOperation(ASTNode):
    def __init__(self, message):
        self.message = message

class DisplayOperation(ASTNode):
    def __init__(self, variable):
        self.variable = variable

class ScaleOperation(ASTNode):
    def __init__(self, ingredient, factor):
        self.ingredient = ingredient
        self.factor = factor

class AddOperation(ASTNode):
    def __init__(self, ingredient, target):
        self.ingredient = ingredient
        self.target = target

class RepeatStatement(ASTNode):
    def __init__(self, count, body):
        self.count = count
        self.body = body

class WhenStatement(ASTNode):
    def __init__(self, condition, then_body, else_body=None):
        self.condition = condition
        self.then_body = then_body
        self.else_body = else_body

class BinaryOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Number(ASTNode):
    def __init__(self, value):
        self.value = value

class String(ASTNode):
    def __init__(self, value):
        self.value = value

class Identifier(ASTNode):
    def __init__(self, name):
        self.name = name

class Value(ASTNode):
    def __init__(self, number, unit=None):
        self.number = number
        self.unit = unit

class InputStatement(ASTNode):
    def __init__(self, var_name):
        self.var_name = var_name

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[0] if tokens else None
    
    def error(self, msg):
        if self.current_token:
            raise Exception(f"Syntax Error at line {self.current_token.line}: {msg}")
        raise Exception(f"Syntax Error: {msg}")
    
    def advance(self):
        """Move to next token"""
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None
    
    def expect(self, token_type):
        """Consume expected token type"""
        if not self.current_token or self.current_token.type != token_type:
            self.error(f"Expected {token_type}, got {self.current_token.type if self.current_token else 'EOF'}")
        token = self.current_token
        self.advance()
        return token
    
    def parse(self):
        """Parse entire program"""
        statements = []
        while self.current_token and self.current_token.type != TokenType.EOF:
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        return Program(statements)
    
    def parse_statement(self):
        """Parse a single statement"""
        if not self.current_token or self.current_token.type == TokenType.EOF:
            return None
        
        # Input statement
        if self.current_token.type == TokenType.INPUT:
            return self.parse_input()
        
        # Declaration
        if self.current_token.type in [TokenType.INGREDIENT, TokenType.TIME, 
                                       TokenType.TEMP, TokenType.QUANTITY, TokenType.TEXT]:
            return self.parse_declaration()
        
        # Operations
        if self.current_token.type == TokenType.MIX:
            return self.parse_mix()
        if self.current_token.type == TokenType.HEAT:
            return self.parse_heat()
        if self.current_token.type == TokenType.WAIT:
            return self.parse_wait()
        if self.current_token.type == TokenType.SERVE:
            return self.parse_serve()
        if self.current_token.type == TokenType.DISPLAY:
            return self.parse_display()
        if self.current_token.type == TokenType.SCALE:
            return self.parse_scale()
        if self.current_token.type == TokenType.ADD:
            return self.parse_add()
        
        # Control flow
        if self.current_token.type == TokenType.REPEAT:
            return self.parse_repeat()
        if self.current_token.type == TokenType.WHEN:
            return self.parse_when()
        
        # Assignment
        if self.current_token.type == TokenType.IDENTIFIER:
            return self.parse_assignment()
        
        self.error(f"Unexpected token: {self.current_token.type}")
    
    def parse_input(self):
        """Parse input statement"""
        self.expect(TokenType.INPUT)
        var_name = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.SEMICOLON)
        return InputStatement(var_name)
    
    def parse_declaration(self):
        """Parse variable declaration"""
        var_type = self.current_token.type
        self.advance()
        
        name = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.ASSIGN)
        value = self.parse_value()
        self.expect(TokenType.SEMICOLON)
        
        return Declaration(var_type, name, value)
    
    def parse_assignment(self):
        """Parse assignment statement"""
        name = self.current_token.value
        self.advance()
        self.expect(TokenType.ASSIGN)
        value = self.parse_value()
        self.expect(TokenType.SEMICOLON)
        
        return Assignment(name, value)
    
    def parse_value(self):
        """Parse a value (number with optional unit or expression)"""
        # Try to parse as expression first (handles arithmetic)
        expr = self.parse_expression()
        
        # Check if there's a unit after the expression
        if self.current_token and self.current_token.type in [
            TokenType.CUPS, TokenType.TBSP, TokenType.TSP, TokenType.ML, TokenType.OZ,
            TokenType.GRAMS, TokenType.LBS, TokenType.FAHRENHEIT, TokenType.CELSIUS,
            TokenType.MINUTES, TokenType.SECONDS, TokenType.HOURS
        ]:
            unit = self.current_token.type
            self.advance()
            # Wrap expression with unit
            return Value(expr, unit)
        
        return expr
    
    def parse_mix(self):
        """Parse mix operation"""
        self.expect(TokenType.MIX)
        ingredients = [self.expect(TokenType.IDENTIFIER).value]
        
        while self.current_token and self.current_token.type == TokenType.WITH:
            self.advance()
            ingredients.append(self.expect(TokenType.IDENTIFIER).value)
        
        self.expect(TokenType.SEMICOLON)
        return MixOperation(ingredients)
    
    def parse_heat(self):
        """Parse heat operation"""
        self.expect(TokenType.HEAT)
        target = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.TO)
        temperature = self.parse_value()
        self.expect(TokenType.SEMICOLON)
        
        return HeatOperation(target, temperature)
    
    def parse_wait(self):
        """Parse wait operation"""
        self.expect(TokenType.WAIT)
        duration = self.parse_value()
        self.expect(TokenType.SEMICOLON)
        
        return WaitOperation(duration)
    
    def parse_serve(self):
        """Parse serve operation"""
        self.expect(TokenType.SERVE)
        message = self.expect(TokenType.STRING).value
        self.expect(TokenType.SEMICOLON)
        
        return ServeOperation(message)
    
    def parse_display(self):
        """Parse display operation"""
        self.expect(TokenType.DISPLAY)
        variable = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.SEMICOLON)
        
        return DisplayOperation(variable)
    
    def parse_scale(self):
        """Parse scale operation"""
        self.expect(TokenType.SCALE)
        ingredient = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.BY)
        factor = self.expect(TokenType.NUMBER).value
        self.expect(TokenType.SEMICOLON)
        
        return ScaleOperation(ingredient, factor)
    
    def parse_add(self):
        """Parse add operation"""
        self.expect(TokenType.ADD)
        ingredient = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.TO)
        target = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.SEMICOLON)
        
        return AddOperation(ingredient, target)
    
    def parse_repeat(self):
        """Parse repeat statement"""
        self.expect(TokenType.REPEAT)
        count = self.expect(TokenType.NUMBER).value
        self.expect(TokenType.TIMES)
        self.expect(TokenType.LBRACE)
        
        body = []
        while self.current_token and self.current_token.type != TokenType.RBRACE:
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
        
        self.expect(TokenType.RBRACE)
        return RepeatStatement(count, body)
    
    def parse_when(self):
        """Parse when statement"""
        self.expect(TokenType.WHEN)
        condition = self.parse_condition()
        self.expect(TokenType.THEN)
        self.expect(TokenType.LBRACE)
        
        then_body = []
        while self.current_token and self.current_token.type != TokenType.RBRACE:
            stmt = self.parse_statement()
            if stmt:
                then_body.append(stmt)
        
        self.expect(TokenType.RBRACE)
        
        else_body = None
        if self.current_token and self.current_token.type == TokenType.ELSE:
            self.advance()
            self.expect(TokenType.LBRACE)
            else_body = []
            while self.current_token and self.current_token.type != TokenType.RBRACE:
                stmt = self.parse_statement()
                if stmt:
                    else_body.append(stmt)
            self.expect(TokenType.RBRACE)
        
        return WhenStatement(condition, then_body, else_body)
    
    def parse_condition(self):
        """Parse condition expression"""
        left = self.parse_expression()
        
        if self.current_token and self.current_token.type in [
            TokenType.EQ, TokenType.NEQ, TokenType.GT, TokenType.LT, TokenType.GTE, TokenType.LTE
        ]:
            op = self.current_token.type
            self.advance()
            right = self.parse_expression()
            return BinaryOp(left, op, right)
        
        return left
    
    def parse_expression(self):
        """Parse arithmetic expression"""
        left = self.parse_term()
        
        while self.current_token and self.current_token.type in [TokenType.PLUS, TokenType.MINUS]:
            op = self.current_token.type
            self.advance()
            right = self.parse_term()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_term(self):
        """Parse term (multiplication/division)"""
        left = self.parse_factor()
        
        while self.current_token and self.current_token.type in [TokenType.MULTIPLY, TokenType.DIVIDE]:
            op = self.current_token.type
            self.advance()
            right = self.parse_factor()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_factor(self):
        """Parse factor (number, identifier, or parenthesized expression)"""
        if self.current_token.type == TokenType.NUMBER:
            value = self.current_token.value
            self.advance()
            return Number(value)
        
        if self.current_token.type == TokenType.IDENTIFIER:
            name = self.current_token.value
            self.advance()
            return Identifier(name)
        
        if self.current_token.type == TokenType.LPAREN:
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return expr
        
        self.error(f"Unexpected token in expression: {self.current_token.type}")
