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
from pysh.files import builtin_cat, builtin_head, builtin_wc
from pysh.system import builtin_sysinfo
from pysh.download import builtin_download
from pysh.colors import BLUE, GREEN, RESET


BUILTINS = {
    'cd': builtin_cd,
    'pwd': builtin_pwd,
    'echo': builtin_echo,
    'help': builtin_help,
    'exit': builtin_exit,
    'procinfo': builtin_procinfo,
    'cat': builtin_cat,
    'head': builtin_head,
    'wc': builtin_wc,
    'sysinfo': builtin_sysinfo,
    'download': builtin_download,
}


def _parse_redirects(args):
    """
    Scan args for > >> < redirect tokens and return them separately.
    Returns (clean_args, out_file, append, in_file).
    """
    clean, out_file, in_file, append = [], None, None, False
    i = 0
    while i < len(args):
        if args[i] in ('>', '>>') and i + 1 < len(args):
            append = args[i] == '>>'
            out_file = args[i + 1]
            i += 2
        elif args[i] == '<' and i + 1 < len(args):
            in_file = args[i + 1]
            i += 2
        else:
            clean.append(args[i])
            i += 1
    return clean, out_file, append, in_file


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


def execute(command, args, background=False):
    """
    Execute a command with the given arguments.

    First checks if the command is a built-in. If not, tries to run it
    as an external program using subprocess (without shell=True).
    Supports I/O redirection (> >> <) and background execution (&).
    """
    if not command:
        return 0

    args, out_file, append, in_file = _parse_redirects(args)

    if command in BUILTINS:
        old_stdout, old_stdin = sys.stdout, sys.stdin
        try:
            if out_file:
                sys.stdout = open(out_file, 'a' if append else 'w')
            if in_file:
                sys.stdin = open(in_file, 'r')
            return BUILTINS[command](args)
        finally:
            if out_file and sys.stdout is not old_stdout:
                sys.stdout.close()
                sys.stdout = old_stdout
            if in_file and sys.stdin is not old_stdin:
                sys.stdin.close()
                sys.stdin = old_stdin

    stdout_fd = None
    stdin_fd = None
    try:
        if out_file:
            stdout_fd = open(out_file, 'a' if append else 'w')
        if in_file:
            stdin_fd = open(in_file, 'r')

        if background:
            proc = subprocess.Popen(
                [command] + args,
                stdout=stdout_fd or subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                stdin=stdin_fd or subprocess.DEVNULL,
            )
            print(f"[{proc.pid}] {command}")
            return 0

        result = subprocess.run(
            [command] + args,
            stdout=stdout_fd or subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=stdin_fd,
            text=True,
        )
        if stdout_fd is None and result.stdout:
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
    finally:
        if stdout_fd:
            stdout_fd.close()
        if stdin_fd:
            stdin_fd.close()


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

            # Detect trailing & for background execution
            background = False
            if line.rstrip().endswith('&'):
                background = True
                line = line.rstrip()[:-1]

            command, args = parse(line)

            if command is None:
                continue

            execute(command, args, background=background)

        except EOFError:
            print("\nGoodbye!")
            break

        except KeyboardInterrupt:
            print()
            continue

        except SystemExit:
            break


if __name__ == '__main__':
    main()
