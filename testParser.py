import unittest

from errors import InterpreterError
from lexer import Lexer, Token
from parser import Parser, Number, Bool, Identifier, BinaryOp, UnaryOp, FunctionDef, FunctionCall, Lambda


class TestParser(unittest.TestCase):
    def setUp(self):
        """
        Set up the parser with an empty token list before each test.
        """
        self.parser = Parser([])

    def parse(self, tokens):
        """
        Helper method to parse a list of tokens and return the first AST node.
        """
        self.parser.tokens = tokens
        return self.parser.parse()[0]  # Get the first (and usually only) AST node

    def test_parse_error_with_context(self):
        tokens = [
            Token('DEFUN', 'Defun', 1, 0),
            Token('LCURLY', '{', 1, 6),
            Token('STRING', "'name'", 1, 7),
            Token('COLON', ':', 1, 13),
            Token('STRING', "'add'", 1, 15),
            Token('COMMA', ',', 1, 20),
            Token('STRING', "'arguments'", 1, 22),
            Token('COLON', ':', 1, 33),
            Token('LPAREN', '(', 1, 35),
            Token('ID', 'x', 1, 36),
            Token('COMMA', ',', 1, 37),
            Token('ID', 'y', 1, 39),
            Token('RPAREN', ')', 1, 40),
            # Missing closing curly brace
        ]
        with self.assertRaises(InterpreterError) as context:
            self.parse(tokens)

        error_message = str(context.exception)
        self.assertIn("Expected '}' to close function definition", error_message)
        self.assertIn("Defun { 'name' : 'add' , 'arguments' : ( x , y )", error_message)
        self.assertIn("^", error_message)

    def test_parse_number(self):
        """
        Test if the parser correctly parses a number token.
        """
        ast = self.parse([Token('NUMBER', 42, 1, 0)])
        self.assertIsInstance(ast, Number)
        self.assertEqual(ast.value, 42)

    def test_parse_boolean(self):
        """
        Test if the parser correctly parses a boolean token.
        """
        ast = self.parse([Token('BOOL', True, 1, 0)])
        self.assertIsInstance(ast, Bool)
        self.assertEqual(ast.value, True)

    def test_parse_identifier(self):
        """
        Test if the parser correctly parses an identifier token.
        """
        ast = self.parse([Token('ID', 'x', 1, 0)])
        self.assertIsInstance(ast, Identifier)
        self.assertEqual(ast.name, 'x')

    def test_parse_binary_operation(self):
        """
        Test if the parser correctly parses a binary operation.
        """
        tokens = [
            Token('NUMBER', 2, 1, 0),
            Token('OP', '+', 1, 2),
            Token('NUMBER', 3, 1, 4)
        ]
        ast = self.parse(tokens)
        self.assertIsInstance(ast, BinaryOp)
        self.assertEqual(ast.op, '+')
        self.assertIsInstance(ast.left, Number)
        self.assertIsInstance(ast.right, Number)

    def test_parse_unary_operation(self):
        """
        Test if the parser correctly parses a unary operation.
        """
        tokens = [Token('BOOL_OP', 'not', 1, 0), Token('BOOL', True, 1, 4)]
        ast = self.parse(tokens)
        self.assertIsInstance(ast, UnaryOp)
        self.assertEqual(ast.op, 'not')
        self.assertIsInstance(ast.operand, Bool)

    def test_parse_function_definition(self):
        """
        Test if the parser correctly parses a function definition.
        """
        tokens = [
            Token('DEFUN', 'Defun', 1, 0),
            Token('LCURLY', '{', 1, 6),
            Token('STRING', "'name'", 1, 7),
            Token('COLON', ':', 1, 13),
            Token('STRING', "'add'", 1, 15),
            Token('COMMA', ',', 1, 20),
            Token('STRING', "'arguments'", 1, 22),
            Token('COLON', ':', 1, 33),
            Token('LPAREN', '(', 1, 35),
            Token('ID', 'x', 1, 36),
            Token('COMMA', ',', 1, 37),
            Token('ID', 'y', 1, 39),
            Token('RPAREN', ')', 1, 40),
            Token('RCURLY', '}', 1, 42),
            Token('ID', 'x', 1, 44),
            Token('OP', '+', 1, 46),
            Token('ID', 'y', 1, 48)
        ]
        ast = self.parse(tokens)
        self.assertIsInstance(ast, FunctionDef)
        self.assertEqual(ast.name, 'add')
        self.assertEqual(ast.params, ['x', 'y'])
        self.assertIsInstance(ast.body, BinaryOp)

    def test_parse_function_call(self):
        """
        Test if the parser correctly parses a function call.
        """
        tokens = [
            Token('ID', 'add', 1, 0),
            Token('LPAREN', '(', 1, 3),
            Token('NUMBER', 2, 1, 4),
            Token('COMMA', ',', 1, 5),
            Token('NUMBER', 3, 1, 7),
            Token('RPAREN', ')', 1, 8)
        ]
        ast = self.parse(tokens)
        self.assertIsInstance(ast, FunctionCall)
        self.assertEqual(ast.name, 'add')
        self.assertEqual(len(ast.args), 2)
        self.assertIsInstance(ast.args[0], Number)
        self.assertIsInstance(ast.args[1], Number)

    def test_parse_lambda(self):
        """
        Test if the parser correctly parses a lambda expression.
        """
        tokens = [
            Token('LAMBDA', 'Lambda', 1, 0),
            Token('LPAREN', '(', 1, 6),
            Token('ID', 'x', 1, 7),
            Token('RPAREN', ')', 1, 8),
            Token('ID', 'x', 1, 10),
            Token('OP', '+', 1, 12),
            Token('NUMBER', 1, 1, 14)
        ]
        ast = self.parse(tokens)
        self.assertIsInstance(ast, Lambda)
        self.assertEqual(ast.params, ['x'])
        self.assertIsInstance(ast.body, BinaryOp)


if __name__ == '__main__':
    unittest.main()



