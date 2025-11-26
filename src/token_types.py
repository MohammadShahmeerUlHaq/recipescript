"""
Token types for RecipeScript language
"""

from enum import Enum, auto

class TokenType(Enum):
    # Data types
    INGREDIENT = auto()
    TIME = auto()
    TEMP = auto()
    QUANTITY = auto()
    TEXT = auto()
    
    # Operations
    MIX = auto()
    HEAT = auto()
    WAIT = auto()
    SERVE = auto()
    SCALE = auto()
    ADD = auto()
    REMOVE = auto()
    DISPLAY = auto()
    
    # Control flow
    REPEAT = auto()
    FOREACH = auto()
    WHEN = auto()
    THEN = auto()
    ELSE = auto()
    TIMES = auto()
    IN = auto()
    
    # Input/Output
    INPUT = auto()
    
    # Prepositions
    TO = auto()
    WITH = auto()
    FOR = auto()
    AT = auto()
    FROM = auto()
    BY = auto()
    
    # Units - Volume
    CUPS = auto()
    TBSP = auto()
    TSP = auto()
    ML = auto()
    OZ = auto()
    
    # Units - Weight
    GRAMS = auto()
    LBS = auto()
    
    # Units - Temperature
    FAHRENHEIT = auto()
    CELSIUS = auto()
    
    # Units - Time
    MINUTES = auto()
    SECONDS = auto()
    HOURS = auto()
    
    # Operators
    ASSIGN = auto()
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    EQ = auto()
    NEQ = auto()
    GT = auto()
    LT = auto()
    GTE = auto()
    LTE = auto()
    
    # Delimiters
    SEMICOLON = auto()
    COMMA = auto()
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    
    # Literals
    NUMBER = auto()
    STRING = auto()
    IDENTIFIER = auto()
    
    # Special
    COMMENT = auto()
    EOF = auto()
    NEWLINE = auto()

class Token:
    def __init__(self, type, value, line=0, column=0):
        self.type = type
        self.value = value
        self.line = line
        self.column = column
    
    def __repr__(self):
        return f"Token({self.type}, {self.value}, {self.line}:{self.column})"
    
    def __str__(self):
        return self.__repr__()

# Keyword mapping
KEYWORDS = {
    'ingredient': TokenType.INGREDIENT,
    'time': TokenType.TIME,
    'temp': TokenType.TEMP,
    'quantity': TokenType.QUANTITY,
    'text': TokenType.TEXT,
    'mix': TokenType.MIX,
    'heat': TokenType.HEAT,
    'wait': TokenType.WAIT,
    'serve': TokenType.SERVE,
    'scale': TokenType.SCALE,
    'add': TokenType.ADD,
    'remove': TokenType.REMOVE,
    'display': TokenType.DISPLAY,
    'repeat': TokenType.REPEAT,
    'foreach': TokenType.FOREACH,
    'when': TokenType.WHEN,
    'then': TokenType.THEN,
    'else': TokenType.ELSE,
    'times': TokenType.TIMES,
    'in': TokenType.IN,
    'input': TokenType.INPUT,
    'to': TokenType.TO,
    'with': TokenType.WITH,
    'for': TokenType.FOR,
    'at': TokenType.AT,
    'from': TokenType.FROM,
    'by': TokenType.BY,
    'cups': TokenType.CUPS,
    'tbsp': TokenType.TBSP,
    'tsp': TokenType.TSP,
    'ml': TokenType.ML,
    'oz': TokenType.OZ,
    'grams': TokenType.GRAMS,
    'lbs': TokenType.LBS,
    'F': TokenType.FAHRENHEIT,
    'C': TokenType.CELSIUS,
    'minutes': TokenType.MINUTES,
    'seconds': TokenType.SECONDS,
    'hours': TokenType.HOURS,
}
