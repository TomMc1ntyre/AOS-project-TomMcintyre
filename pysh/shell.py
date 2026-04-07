"""
pysh — A minimal shell built in Python.

This is the main module. It runs the shell loop:
  1. Display a prompt
  2. Read a line of input
  3. Parse it into a command and arguments
  4. Execute the command
  5. Repeat
"""

import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import grp
    HAS_GRP = True
except ImportError:
    HAS_GRP = False

from pysh.builtins import (
    builtin_cd,
    builtin_echo,
    builtin_exit,
    builtin_help,
    builtin_procinfo,
    builtin_pwd,
)
from pysh.colors import BLUE, GREEN, RESET


BUILTINS = {
    'cd': builtin_cd,
    'pwd': builtin_pwd,
    'echo': builtin_echo,
    'help': builtin_help,
    'exit': builtin_exit,
    'procinfo': builtin_procinfo,
}


def prompt():
    """Return the shell prompt string showing the current directory."""
    cwd = os.getcwd()
    home = os.path.expanduser('~')
    if cwd.startswith(home):
        cwd = '~' + cwd[len(home):]
    
    user = os.environ.get("USER", os.environ.get("USERNAME", "user"))
    
    if HAS_GRP:
        try:
            group = grp.getgrgid(os.getgid()).gr_name
            return f"{GREEN}{user}@{group}{RESET}:{BLUE}{cwd}{RESET}$ "
        except Exception:
            pass
    
    return f"{GREEN}{user}@pysh{RESET}:{BLUE}{cwd}{RESET}$ "


def parse(line):
    """
    Parse a line of input into a command name and a list of arguments.

    Example:
        parse("echo hello world") returns ("echo", ["hello", "world"])
        parse("") returns (None, None)
    """
    if not line or not line.strip():
        return None, None
    parts = line.strip().split()
    return parts[0], parts[1:] if len(parts) > 1 else []


def execute(command, args):
    """
    Execute a command with the given arguments.

    First checks if the command is a built-in. If not, tries to run it
    as an external program using subprocess (without shell=True).
    """
    if not command:
        return 0
    
    if command in BUILTINS:
        return BUILTINS[command](args)
    
    try:
        result = subprocess.run(
            [command] + args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.stdout:
            print(result.stdout, end='')
        if result.stderr:
            print(result.stderr, end='', file=sys.stderr)
        return result.returncode
        
    except FileNotFoundError:
        print(f"pysh: {command}: command not found", file=sys.stderr)
        return 127
    except PermissionError:
        print(f"pysh: {command}: permission denied", file=sys.stderr)
        return 126
    except Exception as e:
        print(f"pysh: {command}: {e}", file=sys.stderr)
        return 1


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

            if command is None:
                continue

            execute(command, args)

        except EOFError:
            print("\nGoodbye!")
            break

        except KeyboardInterrupt:
            print()
            continue

        except SystemExit:
            break


import sys
