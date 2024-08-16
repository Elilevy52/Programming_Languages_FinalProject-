class InterpreterError(Exception):
    """
    Custom exception class for interpreter errors.
    Includes line, column, and context information for detailed error reporting.

    Attributes:
        message (str): The error message.
        line (int, optional): The line number where the error occurred.
        column (int, optional): The column number where the error occurred.
        context (str, optional): The context of the code where the error occurred.
    """

    def __init__(self, message, line=None, column=None, context=None):
        """
        Initializes the InterpreterError with a message and optional line, column, and context information.

        Parameters:
            message (str): The error message.
            line (int, optional): The line number where the error occurred.
            column (int, optional): The column number where the error occurred.
            context (str, optional): The context of the code where the error occurred.
        """
        self.message = message
        self.line = line
        self.column = column
        self.context = context

    def __str__(self):
        """
        Returns the string representation of the error, including the message, line, column, and context.

        Returns:
            str: The formatted error message.
        """
        error_msg = f"Error at line {self.line}, column {self.column}: {self.message}"
        if self.context:
            error_msg += f"\n\n{self.context}\n{' ' * (self.column - 1)}^"
        return error_msg
