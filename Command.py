"""
Command module.

This module defines the Command class, which represents a command with a specific function and a parameter count.

Classes:
    Command: Represents a command with a specific function and a parameter count.
"""

class Command:
    """
    Represents a command with a specific function and a parameter count.

    Attributes:
        command (callable): A callable function that can be executed when required.
        param_count (int): The number of parameters the command expects.
    """

    def __init__(self, command, param_count):
        """
        Initializes a Command instance.

        Args:
            command (callable): The function to be executed by the command.
            param_count (int): The number of parameters the command expects.
        """

        self.command = command
        self.param_count = param_count