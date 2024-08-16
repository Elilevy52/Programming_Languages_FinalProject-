# Functional Programming Interpreter

## Overview
This project is a functional programming interpreter developed as part of a final project for the Programming Language course under Dr. Sharon Yalov-Handzel. The interpreter is designed to handle a simple functional programming language that supports function definitions, lambda expressions, recursion, and various operations, while enforcing immutability and avoiding variable assignments.

## Features
* **Data Types**
  * **INTEGER:**  Supports whole numbers (e.g., -3, 0, 42).
  * **BOOLEAN:** Supports 'True' and 'False'.
* **Operations**
   * **Arithmetic Operations:** Addition ('+'), Subtraction ('-'), Multiplication ('*'), Division ('/'), and Modulo ('%').
   * **Boolean Operations:** AND ('&&'), OR ('||'), NOT ('!').
   * **Comparison Operations:** Equal to ('=='), Not equal to ('!='), Greater than ('>'), Less than ('<'), Greater than or equal to ('>='), Less than or equal to ('<=').
* **Functions**
  * Support for named function definitions and anonymous functions (lambda expressions).
  * Function application, including support for higher-order functions.
  * Recursive function calls, including support for replacing traditional while loops.
* **Immutability**
   * No variable assignments or state changes.

## User Guide for Running the Interpreter

### 1. Interactive Mode (REPL)

#### Steps to Start REPL:
1. **Run the `main.py` script:**
   ```bash
   python main.py
2. **Chose REPL:**
   * When prompted with the main menu, enter '2' to start the REPL.
   * The prompt will change to '>', indicating that the REPL is ready for input.
3. **Enter Commands:**
   * Type your code and press Enter. The interpreter will evaluate the code and display the result.
   * To exit REPL, type 'exit' and press Enter.
# Acknowledgements
 * Dr. Sharon Yalov-Handzel for guidance and support throughout the course and this project.
 * Creators: Eli Levy - 206946790 and Nimrod Bar - 203531801.
