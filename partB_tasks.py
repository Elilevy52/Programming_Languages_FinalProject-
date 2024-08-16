# partB_tasks.py

# Task 1: Fibonacci Sequence Generator
fibonacci = lambda n: (lambda f: f(f, n))(lambda f, n: [0] if n == 0 else [0, 1] if n == 1 else (lambda x: x + [x[-1] + x[-2]])(f(f, n-1)))


def run_fibonacci(n):
    result = fibonacci(n)
    print(f"Fibonacci sequence for n={n}: {result}")


# Task 2: Concatenate Strings
concatenate_strings = lambda strings: (lambda f, s: f(f, s))(lambda f, s: s[0] if len(s) == 1 else s[0] + ' ' + f(f, s[1:]), strings)


def run_concatenate_strings(strings):
    result = concatenate_strings(strings)
    print(f"Concatenated string: '{result}'")


# Task 3: Cumulative Sum of Squares
cumulative_sum_of_squares = lambda lst: [sum(map(lambda x: x*x, filter(lambda x: x % 2 == 0, sublist))) for sublist in lst]


def run_cumulative_sum_of_squares(lst):
    result = cumulative_sum_of_squares(lst)
    print(f"Cumulative sum of squares: {result}")


# Task 4: Higher-Order Function for Cumulative Operations
cumulative_operation = lambda op: lambda seq: seq[0] if len(seq) == 1 else (lambda f, s: s[0] if len(s) == 1 else op(s[0], f(f, s[1:])))(lambda f, s: f(f, s), seq)

def factorial(seq):
    result = 1
    for num in seq:
        result *= num
    return result

def exponentiation(seq):
    result = seq[0]
    for num in seq[1:]:
        result **= num
    return result

def run_cumulative_operations(seq):
    fact_result = factorial(seq)
    expo_result = exponentiation(seq)
    print(f"Factorial result: {fact_result}")
    print(f"Exponentiation result: {expo_result}")

# Task 5: One-Line Filter, Map, Reduce
from functools import reduce
one_line_filter_map_reduce = lambda nums: reduce(lambda x, y: x + y, map(lambda x: x**2, filter(lambda x: x % 2 == 0, nums)))


def run_one_line_filter_map_reduce(nums):
    result = one_line_filter_map_reduce(nums)
    print(f"Sum of squares of even numbers: {result}")


# Task 6: Count Palindromes
count_palindromes = lambda lst: list(map(lambda sublist: len(list(filter(lambda x: x == x[::-1], sublist))), lst))

def run_count_palindromes(lst):
    result = count_palindromes(lst)
    print(f"Number of palindromes: {result}")


# Task 7: Lazy Evaluation Explanation
def lazy_evaluation_example():
    def generate_values():
        print('Generating values...')
        yield 1
        yield 2
        yield 3

    def square(x):
        print(f'Squaring {x}')
        return x * x

    print('Eager evaluation:')
    values = list(generate_values())
    squared_values = [square(x) for x in values]
    print(squared_values)

    print('\nLazy evaluation:')
    squared_values = [square(x) for x in generate_values()]
    print(squared_values)


# Task 8: Prime Numbers Filtering
is_prime = lambda num: num > 1 and all(num % i != 0 for i in range(2, int(num ** 0.5) + 1))
filter_primes = lambda lst: sorted([x for x in lst if is_prime(x)], reverse=True)

def run_filter_primes(lst):
    result = filter_primes(lst)
    print(f"Filtered and sorted prime numbers: {result}")
