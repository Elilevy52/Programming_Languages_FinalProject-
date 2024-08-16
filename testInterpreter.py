import unittest
from lexer import Lexer, Token
from parser import Parser, Number, Bool, Identifier, BinaryOp, UnaryOp, FunctionDef, FunctionCall, Lambda
from interpreter import Interpreter, Environment
from errors import InterpreterError


class TestInterpreter(unittest.TestCase):
    def setUp(self):
        """
        Set up the lexer, parser, and interpreter before each test.
        """
        self.lexer = Lexer()
        self.parser = Parser([])
        self.interpreter = Interpreter()

    def interpret(self, code):
        """
        Helper method to interpret a string of code.
        """
        tokens = self.lexer.tokenize(code)
        self.parser.tokens = tokens
        ast = self.parser.parse()
        self.interpreter.set_code(code)  # Set the code before evaluation
        return [self.interpreter.evaluate(node) for node in ast]

    def test_arithmetic_operations(self):
        """
        Test if the interpreter correctly evaluates arithmetic operations.
        """
        result = self.interpret("3 + 5 * 2")
        self.assertEqual(result[0], 13)

        result = self.interpret("10 - 2 / 2")
        self.assertEqual(result[0], 9)

        result = self.interpret("10 % 3")
        self.assertEqual(result[0], 1)

    def test_boolean_operations(self):
        """
        Test if the interpreter correctly evaluates boolean operations.
        """
        result = self.interpret("True and False")
        self.assertEqual(result[0], False)

        result = self.interpret("True or False")
        self.assertEqual(result[0], True)

        result = self.interpret("not True")
        self.assertEqual(result[0], False)

    def test_comparison_operations(self):
        """
        Test if the interpreter correctly evaluates comparison operations.
        """
        result = self.interpret("3 == 3")
        self.assertEqual(result[0], True)

        result = self.interpret("3 != 4")
        self.assertEqual(result[0], True)

        result = self.interpret("5 > 2")
        self.assertEqual(result[0], True)

        result = self.interpret("2 < 5")
        self.assertEqual(result[0], True)

        result = self.interpret("5 >= 5")
        self.assertEqual(result[0], True)

        result = self.interpret("2 <= 3")
        self.assertEqual(result[0], True)

    def test_function_definition_and_call(self):
        """
        Test if the interpreter correctly evaluates function definitions and calls.
        """
        code = """
        Defun {'name': 'add', 'arguments': (x, y)} x + y
        add(2, 3)
        """
        result = self.interpret(code)
        self.assertEqual(result[1], 5)

    def test_lambda_expression(self):
        """
        Test if the interpreter correctly evaluates lambda expressions.
        """
        code = """
        (Lambda (x) x + 1)(5)
        """
        result = self.interpret(code)
        self.assertEqual(result[0], 6)

    def test_recursive_function(self):
        """
        Test if the interpreter correctly evaluates recursive functions.
        """
        code = """
        Defun {'name': 'factorial', 'arguments': (n)}
            (n == 0) or (n * factorial(n - 1))
        factorial(5)
        """
        result = self.interpret(code)
        self.assertEqual(result[1], 120)

    def test_error_handling(self):
        """
        Test if the interpreter correctly handles errors.
        """
        with self.assertRaises(InterpreterError):
            self.interpret("5 / 0")

        with self.assertRaises(InterpreterError):
            self.interpret("unknown_variable")

    def test_runtime_error_with_context(self):
        code = """
    Defun {'name': 'divide', 'arguments': (x, y)} x / y
    divide(10, 0)
        """
        with self.assertRaises(InterpreterError) as context:
            self.interpret(code)
        self.assertIn("Division by zero", str(context.exception))
        self.assertIn("x / y", str(context.exception))
        self.assertIn("Line 2:", str(context.exception))


if __name__ == '__main__':
    unittest.main()
