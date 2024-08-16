import unittest
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter
from errors import InterpreterError
from testLexer import TestLexer
from testParser import TestParser
from testInterpreter import TestInterpreter
from partB_tasks import run_fibonacci, run_concatenate_strings, run_cumulative_sum_of_squares, run_cumulative_operations, run_one_line_filter_map_reduce, run_count_palindromes, lazy_evaluation_example, run_filter_primes


def repl():
    lexer = Lexer()
    parser = Parser([])
    interpreter = Interpreter()

    print("Welcome to the REPL. Type 'exit' to quit.")
    while True:
        try:
            text = input('> ')
            if text.strip() == "":
                continue
            if text.strip() == "exit":
                break
            tokens = lexer.tokenize(text)
            parser.tokens = tokens
            ast = parser.parse()
            for node in ast:
                result = interpreter.evaluate(node)
                if result is not None:
                    print(result)
        except InterpreterError as e:
            print(e)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


def execute_file(filename):
    """
    Executes the content of a .lambda file.

    Parameters:
        filename (str): The path to the file to be executed.

    Raises:
        ValueError: If the file does not have a .lambda extension.
    """
    if not filename.endswith('.lambda'):
        raise ValueError("File must have a .lambda extension")

    with open(filename, 'r') as file:
        content = file.read()

    lexer = Lexer()
    parser = Parser([])
    interpreter = Interpreter()

    try:
        tokens = lexer.tokenize(content)
        parser.tokens = tokens
        ast = parser.parse()
        for node in ast:
            result = interpreter.evaluate(node)
            if result is not None:
                print(result)
    except InterpreterError as e:
        print(e)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def run_all_tests():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(TestLexer))
    suite.addTests(loader.loadTestsFromTestCase(TestParser))
    suite.addTests(loader.loadTestsFromTestCase(TestInterpreter))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\n--- Test Results ---")
    print(f"Ran {result.testsRun} tests")
    print(f"Errors: {len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    if result.wasSuccessful():
        print("All tests passed successfully!")
    else:
        print("Some tests failed or had errors.")


def main_menu():
    while True:
        print("\nMain Menu:")
        print("1. Run all tests")
        print("2. Start REPL")
        print("3. Execute a file")
        print("4. Run Fibonacci Sequence Generator")
        print("5. Concatenate Strings")
        print("6. Cumulative Sum of Squares")
        print("7. Higher-Order Function for Cumulative Operations")
        print("8. One-Line Filter, Map, Reduce")
        print("9. Count Palindromes")
        print("10. Lazy Evaluation Example")
        print("11. Filter Prime Numbers")
        print("12. Exit")
        choice = input("Enter your choice (1-12): ")

        if choice == '1':
            run_all_tests()
        elif choice == '2':
            repl()
        elif choice == '3':
            filename = input("Enter the filename to execute: ")
            execute_file(filename)
        elif choice == '4':
            n = int(input("Enter the value of n: "))
            run_fibonacci(n)
        elif choice == '5':
            strings = input("Enter the strings to concatenate, separated by commas: ").split(',')
            run_concatenate_strings(strings)
        elif choice == '6':
            lst = input("Enter lists of numbers, separated by commas (e.g., '1 2 3,4 5 6'): ").split(',')
            lst = [list(map(int, sublist.split())) for sublist in lst]
            run_cumulative_sum_of_squares(lst)
        elif choice == '7':
            seq = list(map(int, input("Enter the sequence of numbers, separated by commas: ").split(',')))
            run_cumulative_operations(seq)
        elif choice == '8':
            nums = list(map(int, input("Enter the list of numbers, separated by commas: ").split(',')))
            run_one_line_filter_map_reduce(nums)
        elif choice == '9':
            lst = input("Enter lists of strings, separated by commas (e.g., 'madam,test,level,world'): ").split(',')
            lst = [sublist.split() for sublist in lst]
            run_count_palindromes(lst)
        elif choice == '10':
            lazy_evaluation_example()
        elif choice == '11':
            lst = list(map(int, input("Enter the list of numbers, separated by commas: ").split(',')))
            run_filter_primes(lst)
        elif choice == '12':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main_menu()

