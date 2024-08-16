import re
from typing import List, Optional, NamedTuple
from errors import InterpreterError


class Token(NamedTuple):
    """
    A simple data structure for storing token information.

    Attributes:
        type (str): The type of the token (e.g., 'NUMBER', 'OP').
        value (str): The value of the token.
        line (int): The line number where the token is found.
        column (int): The column number where the token starts.
    """
    type: str
    value: str
    line: int
    column: int


class Lexer:
    """
    The Lexer class is responsible for tokenizing the input source code.
    It converts a string of source code into a list of tokens that can be parsed by the parser.

    Attributes:
        input (str): The source code input string.
        lines (list): A list of strings, where each string is a line of code.
    """

    def __init__(self):
        """
        Initializes the Lexer with an empty input string.
        """
        self.input = ""

    def tokenize(self, input_string: Optional[str] = None) -> List[Token]:
        """
        Tokenizes the input string into a list of tokens.

        Parameters:
            input_string (str, optional): The source code to tokenize. If not provided,
                                          the current value of self.input will be used.

        Returns:
            List[Token]: A list of Token objects representing the tokenized input.

        Raises:
            InterpreterError: If an unexpected character is encountered.
        """
        if input_string is not None:
            self.input = input_string
            self.lines = self.input.split('\n')

        tokens = []
        token_specification = [
            ('DEFUN', r'\bDefun\b'),  # Function definition keyword
            ('LAMBDA', r'\bLambda\b'),  # Lambda keyword
            ('NUMBER', r'\d+'),  # Integer numbers
            ('BOOL', r'\bTrue\b|\bFalse\b'),  # Boolean values
            ('BOOL_OP', r'and|or|not'),  # Boolean operators
            ('COMP_OP', r'==|!=|<=|>=|<|>'),  # Comparison operators
            ('ID', r'[A-Za-z_]\w*'),  # Identifiers
            ('OP', r'[+\-*/%]'),  # Arithmetic operators
            ('LPAREN', r'\('),  # Left parenthesis
            ('RPAREN', r'\)'),  # Right parenthesis
            ('LCURLY', r'\{'),  # Left curly bracket
            ('RCURLY', r'\}'),  # Right curly bracket
            ('COMMA', r','),  # Comma
            ('COLON', r':'),  # Colon
            ('STRING', r'\'[^\']*\'|\"[^\"]*\"'),  # String literals
            ('NEWLINE', r'\n'),  # Line breaks
            ('SKIP', r'[ \t]+'),  # Skip over spaces and tabs
            ('MISMATCH', r'.'),  # Any other character
        ]
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
        line_num = 1
        line_start = 0

        for mo in re.finditer(tok_regex, self.input):
            kind = mo.lastgroup
            value = mo.group()
            column = mo.start() - line_start
            if kind == 'NUMBER':
                value = int(value)
            elif kind == 'BOOL':
                value = True if value == 'True' else False
            elif kind == 'NEWLINE':
                line_start = mo.end()
                line_num += 1
                continue
            elif kind == 'SKIP':
                continue
            elif kind == 'MISMATCH':
                context = self.lines[line_num - 1]
                raise InterpreterError(f"Unexpected character: '{value}'", line_num, column + 1, context)
            tokens.append(Token(kind, value, line_num, column))

        return tokens

    def tokenize_file(self, filename: str) -> List[Token]:
        """
        Tokenizes the content of a file.

        Parameters:
            filename (str): The path to the file to be tokenized.

        Returns:
            List[Token]: A list of Token objects representing the tokenized input.
        """
        with open(filename, 'r') as file:
            self.input = file.read()
        return self.tokenize()
