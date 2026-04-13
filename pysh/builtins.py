"""
Built-in commands for pysh.

Built-in commands are handled directly by the shell, rather than by
running an external program. For example, 'cd' must be a built-in
because changing directory needs to affect the shell process itself.

Each built-in is a function that takes a list of string arguments.
"""

import os
import sys

try:
    import psutil
except ImportError:
    psutil = None


def builtin_pwd(args):
    """
    Print the current working directory.
    Usage: pwd
    """
    print(os.getcwd())
    return 0


def builtin_exit(args):
    """
    Exit the shell.
    Usage: exit [code]
    """
    if args:
        try:
            code = int(args[0])
        except ValueError:
            print(f"exit: invalid exit code: {args[0]}", file=sys.stderr)
            code = 1
    else:
        code = 0
    raise SystemExit(code)


def builtin_cd(args):
    """
    Change the current working directory.
    Usage: cd [path]
    """
    if not args:
        target = os.path.expanduser("~")
    elif len(args) == 1:
        target = args[0]
    else:
        print("cd: too many arguments", file=sys.stderr)
        return 1
    
    try:
        os.chdir(target)
    except FileNotFoundError:
        print(f"cd: {target}: No such file or directory", file=sys.stderr)
        return 1
    except NotADirectoryError:
        print(f"cd: {target}: Not a directory", file=sys.stderr)
        return 1
    except PermissionError:
        print(f"cd: {target}: Permission denied", file=sys.stderr)
        return 1
    return 0


def builtin_echo(args):
    """
    Print text to stdout.
    Usage: echo [text...]
    """
    print(' '.join(args))
    return 0


def builtin_help(args):
    """
    Display help information.
    Usage: help
    """
    help_text = """
Available built-in commands:
  cd <path>       Change directory
  pwd             Print working directory
  echo <text>     Print text to stdout
  help            Show this help message
  exit [code]     Exit the shell
  procinfo <pid>  Show process information (requires psutil)
  cat <file>      Print file contents
  head [-n N]     Print first N lines of file
  wc <file>       Count lines, words, bytes in file
  sysinfo         Show system info (CPU, memory, top processes)

External commands are also available.
    """
    print(help_text.strip())
    return 0


def builtin_procinfo(args):
    """
    Show detailed information about a process.
    Usage: procinfo <pid>
    Shows: status, memory usage, CPU time, parent PID
    """
    if psutil is None:
        print("procinfo: psutil not installed (run: pip install psutil)", file=sys.stderr)
        return 1
    
    if not args or len(args) != 1:
        print("procinfo: missing pid argument", file=sys.stderr)
        print("Usage: procinfo <pid>", file=sys.stderr)
        return 1
    
    try:
        pid = int(args[0])
    except ValueError:
        print(f"procinfo: '{args[0]}' is not a valid integer", file=sys.stderr)
        return 1
    
    try:
        process = psutil.Process(pid)
    except psutil.NoSuchProcess:
        print(f"procinfo: no such process with pid {pid}", file=sys.stderr)
        return 1
    except psutil.AccessDenied:
        print(f"procinfo: access denied to process {pid}", file=sys.stderr)
        return 1
    
    try:
        name = process.name()
        status = process.status()
        memory_info = process.memory_info()
        cpu_times = process.cpu_times()
        
        try:
            parent = process.parent()
            parent_pid = parent.pid if parent else "N/A"
            parent_name = parent.name() if parent else "N/A"
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            parent_pid = "N/A"
            parent_name = "N/A"
        
        print(f"Process Information for PID {pid}:")
        print("-" * 40)
        print(f"Name:         {name}")
        print(f"Status:       {status}")
        print(f"Parent PID:   {parent_pid} ({parent_name})")
        print(f"Memory RSS:   {memory_info.rss:,} bytes ({memory_info.rss / 1024 / 1024:.2f} MB)")
        print(f"CPU User:     {cpu_times.user:.2f} seconds")
        print(f"CPU System:   {cpu_times.system:.2f} seconds")
    except psutil.NoSuchProcess:
        print(f"procinfo: process {pid} no longer exists", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"procinfo: error - {e}", file=sys.stderr)
        return 1
    
    return 0
