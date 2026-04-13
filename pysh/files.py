"""
File commands for pysh.

Pure Python implementations of common Unix file utilities.
"""

import sys


def builtin_cat(args):
    """
    Concatenate and print files.
    Usage: cat <file> [file2 ...]
    """
    if not args:
        print("cat: missing file operand", file=sys.stderr)
        return 1

    for filepath in args:
        try:
            with open(filepath, 'r') as f:
                sys.stdout.write(f.read())
        except FileNotFoundError:
            print(f"cat: {filepath}: No such file or directory", file=sys.stderr)
            return 1
        except PermissionError:
            print(f"cat: {filepath}: Permission denied", file=sys.stderr)
            return 1
        except IsADirectoryError:
            print(f"cat: {filepath}: Is a directory", file=sys.stderr)
            return 1
        except UnicodeDecodeError:
            print(f"cat: {filepath}: cannot decode file", file=sys.stderr)
            return 1
        except Exception as e:
            print(f"cat: {filepath}: {e}", file=sys.stderr)
            return 1

    return 0


def builtin_head(args):
    """
    Print first N lines of a file.
    Usage: head [-n N] <file>
    Default: 10 lines
    """
    num_lines = 10
    filepath = None

    i = 0
    while i < len(args):
        if args[i] == '-n' and i + 1 < len(args):
            try:
                num_lines = int(args[i + 1])
            except ValueError:
                print(f"head: invalid number: {args[i + 1]}", file=sys.stderr)
                return 1
            i += 2
        elif args[i].startswith('-n') and len(args[i]) > 2:
            try:
                num_lines = int(args[i][2:])
            except ValueError:
                print(f"head: invalid number: {args[i][2:]}", file=sys.stderr)
                return 1
            i += 1
        else:
            filepath = args[i]
            i += 1

    if filepath is None:
        print("head: missing file operand", file=sys.stderr)
        return 1

    try:
        with open(filepath, 'r') as f:
            for _ in range(num_lines):
                line = f.readline()
                if not line:
                    break
                sys.stdout.write(line)
    except FileNotFoundError:
        print(f"head: {filepath}: No such file or directory", file=sys.stderr)
        return 1
    except PermissionError:
        print(f"head: {filepath}: Permission denied", file=sys.stderr)
        return 1
    except IsADirectoryError:
        print(f"head: {filepath}: Is a directory", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"head: {filepath}: {e}", file=sys.stderr)
        return 1

    return 0


def builtin_wc(args):
    """
    Print line, word, and byte counts for files.
    Usage: wc <file> [file2 ...]
    Output: lines words bytes filepath
    """
    if not args:
        print("wc: missing file operand", file=sys.stderr)
        return 1

    total_lines = 0
    total_words = 0
    total_bytes = 0

    for filepath in args:
        try:
            with open(filepath, 'rb') as f:
                content = f.read()
                bytes_count = len(content)
                lines = content.count(b'\n')
                if content and not content.endswith(b'\n'):
                    lines += 1
                words = len(content.split())
        except FileNotFoundError:
            print(f"wc: {filepath}: No such file or directory", file=sys.stderr)
            return 1
        except PermissionError:
            print(f"wc: {filepath}: Permission denied", file=sys.stderr)
            return 1
        except IsADirectoryError:
            print(f"wc: {filepath}: Is a directory", file=sys.stderr)
            return 1
        except Exception as e:
            print(f"wc: {filepath}: {e}", file=sys.stderr)
            return 1

        print(f"{lines:>7} {words:>7} {bytes_count:>7} {filepath}")
        total_lines += lines
        total_words += words
        total_bytes += bytes_count

    if len(args) > 1:
        print(f"{total_lines:>7} {total_words:>7} {total_bytes:>7} total")

    return 0