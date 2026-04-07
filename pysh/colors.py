"""
Color codes for terminal output.

The color codes are ANSI escape codes that can be used to change the color of text printed to the terminal. For example, to print "Hello" in red, you can do:
    print(f"{RED}Hello{RESET}")

ANSI is a standard for terminal control codes, and these codes are widely supported in modern terminals.
The RESET code is used to reset the text color back to the default after printing colored text.
"""

RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
