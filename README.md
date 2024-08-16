# Functional Programming Interpreter

## Overview
This project is a functional programming interpreter developed as part of a final project for the Programming Language course under Dr. Sharon Yalov-Handzel. The interpreter is designed to handle a simple functional programming language that supports function definitions, lambda expressions, recursion, and various operations, while enforcing immutability and avoiding variable assignments.

## Features
* **Data Types**
  * **INTEGER:**  Supports whole numbers (e.g., -3, 0, 42).
  * **BOOLEAN:** Supports <span style="color: green;">`True`</span> and <span style="color: red;">`False`</span>
* **Operations**
   * **Arithmetic Operations:** Addition (`+`), Subtraction (`-`), Multiplication (`*`), Division (`/`), and Modulo (`%`).
   * **Boolean Operations:** AND (`&&`), OR (`||`), NOT (`!`).
   * **Comparison Operations:** Equal to (`==`), Not equal to (`!=`), Greater than (`>`), Less than (`<`), Greater than or equal to (`>=`), Less than or equal to (`<=`).
* **Functions**
  * Support for named function definitions and anonymous functions (lambda expressions).
  * Function application, including support for higher-order functions.
  * Recursive function calls, including support for replacing traditional while loops.
* **Immutability**
   * No variable assignments or state changes.

## User Guide for Running the Interpreter

### 1. Interactive Mode (REPL)
The interpreter can be run in an interactive mode, also known as REPL (Read-Eval-Print Loop), 
where you can enter commands line-by-line and see the results immediately.

**Steps to Start REPL:**
1. **Run the `main.py` script:**
   ```bash
   python main.py
2. **Chose REPL:**
   * When prompted with the main menu, enter `2` to start the REPL.
   * The prompt will change to `>`, indicating that the REPL is ready for input.
3. **Enter Commands:**
   * Type your code and press Enter. The interpreter will evaluate the code and display the result.
   * To exit REPL, type `exit` and press Enter.
**Example Usage in REPL:**
  ```console
  > 3 + 5 * 2
  13
  > Defun {'name': 'add', 'arguments': (x,y)} x + y
  > add(2, 3)
  5
```
### 2. File Execution Mode
You can execute a .lambda file containing a script in the custom language defined by the interpreter.
**Steps to Execute a File:**
 1. **Run the `main.py` script:**
    ```bash
    python main.py
 2. **Chose File Exectuion:**
    * From the main menu, enter `3` to execute a file.
    * Enter the path to your `.lambda` file when prompted.
3. **View Results:**
    * The interpreter will execute the entire file and display the results for each evaluated expression.
 
**Example Script:**
 ```lambda
  Defun {'name': 'factorial', 'arguments': (n)} (n == 0) or (n * factorial(n - 1))
factorial(5)
```
**Expected output:**
```console
120
```
# Acknowledgements
 * Dr. Sharon Yalov-Handzel for guidance and support throughout the course and this project.
 * Creators: Eli Levy - 206946790 and Nimrod Bar - 203531801.
