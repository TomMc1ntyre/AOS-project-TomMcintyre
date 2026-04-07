# pysh - Python Shell

A minimal shell built in Python for the Architecture and Operating Systems module.

## Setup

This project uses [uv](https://docs.astral.sh/uv/) for dependency management.

### Install uv

If you don't have uv installed yet:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Install dependencies

```bash
uv sync
```

### Run the shell

```bash
uv run pysh
```

You should see the pysh prompt. Try typing `pwd` or `ls` to check it works.

## Project Structure

```
pysh/
  __init__.py    — Package marker
  shell.py       — Main loop: prompt, parse input, dispatch commands
  builtins.py    — Built-in command implementations (pwd, exit, etc.)
  colors.py      — ANSI color codes for terminal output
pyproject.toml   — Project configuration and dependencies
test_urls.txt    — Sample URLs for testing the download command
```

## Adding a New Built-in Command

1. Write a function in `builtins.py` (see `builtin_pwd` as an example)
2. Import it in `shell.py` and add an `elif` branch in the `execute` function
3. Run the shell and test it: `uv run pysh`
