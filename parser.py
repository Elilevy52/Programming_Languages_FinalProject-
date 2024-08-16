from lexer import Lexer
from errors import InterpreterError


class ASTNode:
    """
    Base class for all AST nodes.
    """

    def __init__(self, line, column):
        """
        Initializes an AST node with line and column information.

        Parameters:
            line (int): The line number where the node is found.
            column (int): The column number where the node starts.
        """
        self.line = line
        self.column = column


class Number(ASTNode):
    """
    AST node for numeric literals.
    """

    def __init__(self, value, line, column):
        """
        Initializes a Number node.

        Parameters:
            value (int): The numeric value.
            line (int): The line number where the node is found.
            column (int): The column number where the node starts.
        """
        super().__init__(line, column)
        self.value = value


class Bool(ASTNode):
    """
    AST node for boolean literals.
    """

    def __init__(self, value, line, column):
        """
        Initializes a Bool node.

        Parameters:
            value (bool): The boolean value.
            line (int): The line number where the node is found.
            column (int): The column number where the node starts.
        """
        super().__init__(line, column)
        self.value = value


class BinaryOp(ASTNode):
    """
    AST node for binary operations.
    """

    def __init__(self, left, op, right, line, column):
        """
        Initializes a BinaryOp node.

        Parameters:
            left (ASTNode): The left operand of the binary operation.
            op (str): The operator (e.g., '+', '-', '*').
            right (ASTNode): The right operand of the binary operation.
            line (int): The line number where the node is found.
            column (int): The column number where the node starts.
        """
        super().__init__(line, column)
        self.left = left
        self.op = op
        self.right = right


class UnaryOp(ASTNode):
    """
    AST node for unary operations.
    """

    def __init__(self, op, operand, line, column):
        """
        Initializes a UnaryOp node.

        Parameters:
            op (str): The unary operator (e.g., 'not').
            operand (ASTNode): The operand of the unary operation.
            line (int): The line number where the node is found.
            column (int): The column number where the node starts.
        """
        super().__init__(line, column)
        self.op = op
        self.operand = operand


class FunctionDef(ASTNode):
    """
    AST node for function definitions.
    """

    def __init__(self, name, params, body, line, column):
        """
        Initializes a FunctionDef node.

        Parameters:
            name (str): The name of the function.
            params (list): A list of parameter names.
            body (ASTNode): The body of the function.
            line (int): The line number where the node is found.
            column (int): The column number where the node starts.
        """
        super().__init__(line, column)
        self.name = name
        self.params = params
        self.body = body


class Lambda(ASTNode):
    """
    AST node for lambda expressions.
    """

    def __init__(self, params, body, line, column):
        """
        Initializes a Lambda node.

        Parameters:
            params (list): A list of parameter names.
            body (ASTNode): The body of the lambda expression.
            line (int): The line number where the node is found.
            column (int): The column number where the node starts.
        """
        super().__init__(line, column)
        self.params = params
        self.body = body


class FunctionCall(ASTNode):
    """
    AST node for function calls.
    """

    def __init__(self, name, args, line, column):
        """
        Initializes a FunctionCall node.

        Parameters:
            name (str): The name of the function being called.
            args (list): A list of arguments for the function call.
            line (int): The line number where the node is found.
            column (int): The column number where the node starts.
        """
        super().__init__(line, column)
        self.name = name
        self.args = args


class Identifier(ASTNode):
    """
    AST node for identifiers.
    """

    def __init__(self, name, line, column):
        """
        Initializes an Identifier node.

        Parameters:
            name (str): The name of the identifier.
            line (int): The line number where the node is found.
            column (int): The column number where the node starts.
        """
        super().__init__(line, column)
        self.name = name


class Parser:
    """
    The Parser class is responsible for parsing a list of tokens and creating an Abstract Syntax Tree (AST).

    Attributes:
        tokens (list): The list of tokens to parse.
        pos (int): The current position in the token list.
    """

    def __init__(self, tokens):
        """
        Initializes the Parser with a list of tokens.

        Parameters:
            tokens (list): A list of tokens to parse.
        """
        self.tokens = tokens
        self.pos = 0

    def parse(self):
        """
        Parses the list of tokens and returns the corresponding AST.

        Returns:
            list: A list of AST nodes representing the parsed structure of the code.

        Raises:
            InterpreterError: If there is a syntax error in the input tokens.
        """
        self.pos = 0  # Reset position
        result = []
        while self.pos < len(self.tokens):
            result.append(self.parse_statement())
        return result

    def parse_statement(self):
        """
        Parses a single statement from the list of tokens.

        Returns:
            ASTNode: The corresponding AST node for the parsed statement.

        Raises:
            InterpreterError: If there is an unexpected token or syntax error.
        """
        try:
            token = self.tokens[self.pos]
            if token.type == 'DEFUN':
                return self.parse_function_def()
            elif token.type == 'LAMBDA':
                return self.parse_lambda()
            else:
                return self.parse_expression()
        except InterpreterError:
            # Re-raise the error without modifying it
            raise
        except Exception as e:
            context = self.get_context(self.tokens[self.pos])
            raise InterpreterError(f"Unexpected error parsing statement: {str(e)}",
                                   self.tokens[self.pos].line,
                                   self.tokens[self.pos].column,
                                   context)

    def parse_function_def(self):
        """
        Parses a function definition from the list of tokens.

        Returns:
            FunctionDef: An AST node representing the function definition.

        Raises:
            InterpreterError: If there is a syntax error in the function definition.
        """
        start_token = self.tokens[self.pos]
        self.pos += 1  # skip 'Defun'
        if self.pos >= len(self.tokens) or self.tokens[self.pos].type != 'LCURLY':
            context = self.get_context(start_token)
            raise InterpreterError("Expected '{' after 'Defun'", start_token.line, start_token.column, context)
        self.pos += 1  # skip '{'

        if self.pos >= len(self.tokens) or self.tokens[self.pos].type != 'STRING':
            context = self.get_context(self.tokens[self.pos - 1])
            raise InterpreterError("Expected string for function name", self.tokens[self.pos - 1].line,
                                   self.tokens[self.pos - 1].column, context)
        self.pos += 1  # skip 'name' key
        if self.pos >= len(self.tokens) or self.tokens[self.pos].type != 'COLON':
            context = self.get_context(self.tokens[self.pos - 1])
            raise InterpreterError("Expected ':' after 'name'", self.tokens[self.pos - 1].line,
                                   self.tokens[self.pos - 1].column, context)
        self.pos += 1  # skip ':'
        if self.pos >= len(self.tokens) or self.tokens[self.pos].type != 'STRING':
            context = self.get_context(self.tokens[self.pos - 1])
            raise InterpreterError("Expected string for function name", self.tokens[self.pos - 1].line,
                                   self.tokens[self.pos - 1].column, context)
        function_name = self.tokens[self.pos].value.strip("'")
        self.pos += 1  # skip function name

        if self.pos >= len(self.tokens) or self.tokens[self.pos].type != 'COMMA':
            context = self.get_context(self.tokens[self.pos - 1])
            raise InterpreterError("Expected ',' after function name", self.tokens[self.pos - 1].line,
                                   self.tokens[self.pos - 1].column, context)
        self.pos += 1  # skip ','
        if self.pos >= len(self.tokens) or self.tokens[self.pos].type != 'STRING' or self.tokens[
            self.pos].value != "'arguments'":
            context = self.get_context(self.tokens[self.pos - 1])
            raise InterpreterError("Expected 'arguments' key", self.tokens[self.pos - 1].line,
                                   self.tokens[self.pos - 1].column, context)
        self.pos += 1  # skip 'arguments' key
        if self.pos >= len(self.tokens) or self.tokens[self.pos].type != 'COLON':
            context = self.get_context(self.tokens[self.pos - 1])
            raise InterpreterError("Expected ':' after 'arguments'", self.tokens[self.pos - 1].line,
                                   self.tokens[self.pos - 1].column, context)
        self.pos += 1  # skip ':'
        if self.pos >= len(self.tokens) or self.tokens[self.pos].type != 'LPAREN':
            context = self.get_context(self.tokens[self.pos - 1])
            raise InterpreterError("Expected '(' for argument list", self.tokens[self.pos - 1].line,
                                   self.tokens[self.pos - 1].column, context)
        self.pos += 1  # skip '('

        params = []
        while self.pos < len(self.tokens) and self.tokens[self.pos].type != 'RPAREN':
            param_token = self.tokens[self.pos]
            if param_token.type != 'ID':
                context = self.get_context(param_token)
                raise InterpreterError(f"Expected identifier for parameter but got {param_token.value}",
                                       param_token.line, param_token.column, context)
            params.append(param_token.value)
            self.pos += 1
            if self.pos < len(self.tokens) and self.tokens[self.pos].type == 'COMMA':
                self.pos += 1  # skip ','

        if self.pos >= len(self.tokens) or self.tokens[self.pos].type != 'RPAREN':
            context = self.get_context(self.tokens[self.pos - 1])
            raise InterpreterError("Expected ')' to close argument list", self.tokens[self.pos - 1].line,
                                   self.tokens[self.pos - 1].column, context)
        self.pos += 1  # skip ')'
        if self.pos >= len(self.tokens) or self.tokens[self.pos].type != 'RCURLY':
            context = self.get_context(self.tokens[self.pos - 1])
            raise InterpreterError("Expected '}' to close function definition", self.tokens[self.pos - 1].line,
                                   self.tokens[self.pos - 1].column, context)
        self.pos += 1  # skip '}'

        body = self.parse_boolean_expression()  # Parse the entire body as a boolean expression
        return FunctionDef(function_name, params, body, start_token.line, start_token.column)

    def parse_lambda(self):
        """
        Parses a lambda expression.

        Returns:
            Lambda: An AST node representing the lambda expression.

        Raises:
            InterpreterError: If there is a syntax error in the lambda expression.
        """
        start_token = self.tokens[self.pos]
        self.pos += 1  # skip 'Lambda'
        if self.tokens[self.pos].type != 'LPAREN':
            raise InterpreterError("Expected '(' after 'Lambda'", self.tokens[self.pos].line,
                                   self.tokens[self.pos].column)
        params = self.parse_params()
        body = self.parse_expression()
        lambda_node = Lambda(params, body, start_token.line, start_token.column)

        # Check if the lambda is immediately called
        if self.pos < len(self.tokens) and self.tokens[self.pos].type == 'LPAREN':
            return self.parse_function_call(lambda_node)
        return lambda_node

    def parse_params(self):
        """
        Parses the parameters of a function or lambda expression.

        Returns:
            list: A list of parameter names.

        Raises:
            InterpreterError: If there is a syntax error in the parameter list.
        """
        params = []
        if self.pos >= len(self.tokens) or self.tokens[self.pos].type != 'LPAREN':
            raise InterpreterError("Expected '(' at the start of parameters", self.tokens[self.pos - 1].line,
                                   self.tokens[self.pos - 1].column)
        self.pos += 1  # skip '('
        while self.pos < len(self.tokens) and self.tokens[self.pos].type != 'RPAREN':
            if self.tokens[self.pos].type == 'ID':
                param = self.tokens[self.pos]
                params.append(param.value)
                self.pos += 1
            else:
                raise InterpreterError("Expected identifier in parameter list", self.tokens[self.pos].line,
                                       self.tokens[self.pos].column)
            if self.tokens[self.pos].type == 'COMMA':
                self.pos += 1  # skip ','
        if self.pos >= len(self.tokens) or self.tokens[self.pos].type != 'RPAREN':
            raise InterpreterError("Expected ')' at the end of parameters", self.tokens[self.pos - 1].line,
                                   self.tokens[self.pos - 1].column)
        self.pos += 1  # skip ')'
        return params

    def parse_function_call(self, func=None):
        """
        Parses a function call expression.

        Parameters:
            func (ASTNode, optional): The function node if it's a lambda being called immediately.

        Returns:
            FunctionCall: An AST node representing the function call.

        Raises:
            InterpreterError: If there is a syntax error in the function call.
        """
        if func is None:
            start_token = self.tokens[self.pos]
            name = start_token.value
            self.pos += 1  # skip function name
        else:
            start_token = func
            name = func

        args = []
        if self.pos < len(self.tokens) and self.tokens[self.pos].type == 'LPAREN':
            self.pos += 1  # skip '('
            while self.pos < len(self.tokens) and self.tokens[self.pos].type != 'RPAREN':
                args.append(self.parse_expression())
                if self.tokens[self.pos].type == 'COMMA':
                    self.pos += 1  # skip ','
            if self.pos >= len(self.tokens) or self.tokens[self.pos].type != 'RPAREN':
                raise InterpreterError("Expected ')' after arguments in function call", self.tokens[self.pos - 1].line,
                                       self.tokens[self.pos - 1].column)
            self.pos += 1  # skip ')'
        return FunctionCall(name, args, start_token.line, start_token.column)

    def parse_boolean_expression(self):
        """
        Parses a boolean expression.

        Returns:
            ASTNode: The corresponding AST node for the boolean expression.

        Raises:
            InterpreterError: If there is a syntax error in the boolean expression.
        """
        expr = self.parse_comparison()
        while self.pos < len(self.tokens) and self.tokens[self.pos].type == 'BOOL_OP':
            op = self.tokens[self.pos].value
            op_token = self.tokens[self.pos]
            self.pos += 1
            if op == 'not':
                right = self.parse_comparison()
                expr = UnaryOp(op, right, op_token.line, op_token.column)
            else:
                right = self.parse_comparison()
                expr = BinaryOp(expr, op, right, op_token.line, op_token.column)
        return expr

    def parse_comparison(self):
        """
        Parses a comparison expression.

        Returns:
            ASTNode: The corresponding AST node for the comparison expression.

        Raises:
            InterpreterError: If there is a syntax error in the comparison expression.
        """
        expr = self.parse_arithmetic()
        while self.pos < len(self.tokens) and self.tokens[self.pos].type == 'COMP_OP':
            op = self.tokens[self.pos].value
            op_token = self.tokens[self.pos]
            self.pos += 1
            right = self.parse_arithmetic()
            expr = BinaryOp(expr, op, right, op_token.line, op_token.column)
        return expr

    def parse_arithmetic(self):
        """
        Parses an arithmetic expression.

        Returns:
            ASTNode: The corresponding AST node for the arithmetic expression.

        Raises:
            InterpreterError: If there is a syntax error in the arithmetic expression.
        """
        expr = self.parse_term()
        while self.pos < len(self.tokens) and self.tokens[self.pos].type == 'OP' and self.tokens[self.pos].value in [
            '+', '-']:
            op = self.tokens[self.pos].value
            op_token = self.tokens[self.pos]
            self.pos += 1
            right = self.parse_term()
            expr = BinaryOp(expr, op, right, op_token.line, op_token.column)
        return expr

    def parse_term(self):
        """
        Parses a term in an arithmetic expression.

        Returns:
            ASTNode: The corresponding AST node for the term.

        Raises:
            InterpreterError: If there is a syntax error in the term.
        """
        expr = self.parse_factor()
        while self.pos < len(self.tokens) and self.tokens[self.pos].type == 'OP' and self.tokens[self.pos].value in [
            '*', '/', '%']:
            op = self.tokens[self.pos].value
            op_token = self.tokens[self.pos]
            self.pos += 1
            right = self.parse_factor()
            expr = BinaryOp(expr, op, right, op_token.line, op_token.column)
        return expr

    def parse_factor(self):
        """
        Parses a factor in an arithmetic expression.

        Returns:
            ASTNode: The corresponding AST node for the factor.

        Raises:
            InterpreterError: If there is a syntax error in the factor.
        """
        if self.pos >= len(self.tokens):
            raise InterpreterError("Unexpected end of input", self.tokens[-1].line, self.tokens[-1].column)

        token = self.tokens[self.pos]
        if token.type == 'NUMBER':
            self.pos += 1
            return Number(token.value, token.line, token.column)
        elif token.type == 'BOOL':
            self.pos += 1
            return Bool(token.value, token.line, token.column)
        elif token.type == 'LPAREN':
            self.pos += 1  # skip '('
            expr = self.parse_expression()
            if self.pos >= len(self.tokens) or self.tokens[self.pos].type != 'RPAREN':
                raise InterpreterError("Expected ')' to close expression", self.tokens[self.pos - 1].line,
                                       self.tokens[self.pos - 1].column)
            self.pos += 1  # skip ')'
            # Check if this is a function call
            if self.pos < len(self.tokens) and self.tokens[self.pos].type == 'LPAREN':
                return self.parse_function_call(expr)
            return expr
        elif token.type == 'ID':
            self.pos += 1
            if self.pos < len(self.tokens) and self.tokens[self.pos].type == 'LPAREN':
                self.pos -= 1  # go back to parse function call
                return self.parse_function_call()
            return Identifier(token.value, token.line, token.column)
        elif token.type == 'LAMBDA':
            return self.parse_lambda()  # Add this line to handle lambda expressions
        elif token.type == 'BOOL_OP' and token.value == 'not':
            self.pos += 1
            operand = self.parse_factor()
            return UnaryOp('not', operand, token.line, token.column)
        elif token.type == 'OP' and token.value in ['+', '-']:
            op = token.value
            self.pos += 1
            expr = self.parse_factor()
            return UnaryOp(op, expr, token.line, token.column)

        raise InterpreterError(f"Unexpected token: {token.value}", token.line, token.column)

    def parse_expression(self):
        """
        Parses an expression, starting with a boolean expression.

        Returns:
            ASTNode: The corresponding AST node for the expression.

        Raises:
            InterpreterError: If there is a syntax error in the expression.
        """
        return self.parse_boolean_expression()

    def get_context(self, token):
        """
        Retrieves the context around a token for error reporting.

        Parameters:
            token (Token): The token for which context is needed.

        Returns:
            str: A string representing the line of code where the token is found.
        """
        line = self.tokens[0].line
        context = ""
        for t in self.tokens:
            if t.line != line:
                break
            context += t.value + " "
        return context.strip()
