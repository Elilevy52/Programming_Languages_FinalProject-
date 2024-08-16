import unittest

from errors import InterpreterError
from lexer import Lexer, Token

class TestLexer(unittest.TestCase):
    """
    Unit tests for the Lexer class.
    """
    def setUp(self):
        self.lexer = Lexer()

    def test_unexpected_character(self):
        with self.assertRaises(InterpreterError) as context:
            self.lexer.tokenize("Defun {'name': 'add', 'arguments': (x, y)} x @ y")

        error_message = str(context.exception)
        self.assertIn("Unexpected character: '@'", error_message)
        self.assertIn("Defun {'name': 'add', 'arguments': (x, y)} x @ y", error_message)
        self.assertIn("^", error_message)

    def test_tokenize_numbers(self):
        """
        Test if lexer correctly tokenizes numbers.
        """
        tokens = self.lexer.tokenize("123 456")
        self.assertEqual(len(tokens), 2)
        self.assertEqual(tokens[0].type, 'NUMBER')
        self.assertEqual(tokens[0].value, 123)
        self.assertEqual(tokens[1].value, 456)

    def test_tokenize_operators(self):
        """
        Test if lexer correctly tokenizes operators.
        """
        tokens = self.lexer.tokenize("+ - * / %")
        self.assertEqual(len(tokens), 5)
        self.assertTrue(all(token.type == 'OP' for token in tokens))
        self.assertEqual([token.value for token in tokens], ['+', '-', '*', '/', '%'])

    def test_tokenize_comparisons(self):
        """
        Test if lexer correctly tokenizes comparison operators.
        """
        tokens = self.lexer.tokenize("== != < <= > >=")
        self.assertEqual(len(tokens), 6)
        self.assertTrue(all(token.type == 'COMP_OP' for token in tokens))

    def test_tokenize_boolean_ops(self):
        """
        Test if lexer correctly tokenizes boolean operators.
        """
        tokens = self.lexer.tokenize("and or not")
        self.assertEqual(len(tokens), 3)
        self.assertTrue(all(token.type == 'BOOL_OP' for token in tokens))

    def test_tokenize_identifiers(self):
        """
        Test if lexer correctly tokenizes identifiers.
        """
        tokens = self.lexer.tokenize("x y123 _z")
        self.assertEqual(len(tokens), 3)
        self.assertTrue(all(token.type == 'ID' for token in tokens))

    def test_tokenize_keywords(self):
        """
        Test if lexer correctly tokenizes keywords.
        """
        tokens = self.lexer.tokenize("Defun Lambda")
        self.assertEqual(tokens[0].type, 'DEFUN')
        self.assertEqual(tokens[1].type, 'LAMBDA')

    def test_tokenize_complex_expression(self):
        """
        Test if lexer correctly tokenizes a complex expression.
        """
        expr = "Defun {'name': 'add', 'arguments': (x, y)} x + y"
        tokens = self.lexer.tokenize(expr)
        expected_types = ['DEFUN', 'LCURLY', 'STRING', 'COLON', 'STRING', 'COMMA', 'STRING', 'COLON',
                          'LPAREN', 'ID', 'COMMA', 'ID', 'RPAREN', 'RCURLY', 'ID', 'OP', 'ID']
        self.assertEqual([token.type for token in tokens], expected_types)


if __name__ == '__main__':
    unittest.main()
