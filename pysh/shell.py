"""
pysh — A minimal shell built in Python.

This is the main module. It runs the shell loop:
  1. Display a prompt
  2. Read a line of input
  3. Parse it into a command and arguments
  4. Execute the command
  5. Repeat
"""

import grp
import os
import subprocess

from pysh.builtins import builtin_exit, builtin_pwd
from pysh.colors import BLUE, GREEN, RESET


def prompt():
    """Return the shell prompt string showing the current directory."""
    cwd = os.getcwd()
    user = os.environ.get("USER")
    group = grp.getgrgid(os.getgid()).gr_name

    return f"{GREEN}{user}@{group}{RESET}:{BLUE}{cwd}{RESET}$ "


def parse(line):
    """
    Parse a line of input into a command name and a list of arguments.

    Example:
        parse("echo hello world") returns ("echo", ["hello", "world"])
        parse("") returns (None, [])
    """
    parts = line.strip().split()
    if not parts:
        return None, []
    return parts[0], parts[1:]


def execute(command, args):
    """
    Execute a command with the given arguments.

    First checks if the command is a built-in. If not, tries to run it
    as an external program using subprocess.
    """

    # TODO: Add your own built-in commands here
    if command == "pwd":
        builtin_pwd(args)
    elif command == "exit":
        builtin_exit(args)
    else:
        # Run external commands as a child process.
        # subprocess.run will search for the command on the system PATH,
        # run it, and wait for it to finish before returning.
        try:
            subprocess.run([command] + args)
        except FileNotFoundError:
            print(f"pysh: {command}: command not found")


def main():
    """Entry point for the shell."""

    print(
        r"""
 __
 \ \
  \ \
  / /
 /_/   ______
      /_____/"""
    )

    print()
    print("Welcome to pysh! Type 'help' to see available commands.\n")

    while True:
        try:
            line = input(prompt())

            command, args = parse(line)

            # If the user just pressed Enter, show the prompt again
            if command is None:
                continue

            execute(command, args)

        except EOFError:
            # Ctrl+D — exit the shell
            print("\nGoodbye!")
            break

        except KeyboardInterrupt:
            # Ctrl+C — don't exit, just move to a new line
            print()
            continue

        except SystemExit:
            # The exit command was called
            break
