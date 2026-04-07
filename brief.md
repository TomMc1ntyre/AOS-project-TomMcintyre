# Assessment Brief

## CA1 - Project

|                                 |                                    |
| ------------------------------- | ---------------------------------- |
| **Module Name**                 | Architecture and Operating Systems |
| **Lecturer Name**               | Michael McAndrew                   |
| **Title of Brief**              | CA1 - Project                      |
| **Percentage of Overall Grade** | 55%                                |
| **Date handed out**             | Monday 9th March                   |
| **Due date**                    | Sunday 3rd May                     |
| **Individual or Group**         | Individual                         |

## Problem to Solve

A shell is one of the most fundamental pieces of software in any operating system. It is the interface between the user and the kernel, allowing users to launch programs, manage files, and control processes.

In 1989, Brian Fox wrote **Bash** (the Bourne Again Shell) for the GNU project, a free, open source replacement for the proprietary Bourne shell that would go on to become the default shell on nearly every Linux distribution. In this project, you will follow in those footsteps and build your own shell in Python called **`pysh`**, capable of executing commands, managing processes, working with files, and more.

You will be provided with a **starter template** that includes the basic input loop, and project structure.

## Requirements

- Your shell must be written in **Python**. The starter template is provided in Python and must be used as the basis for your project.
- You must **not** use `shell=True` when calling `subprocess.run()` or `subprocess.Popen()`. Your shell must parse commands and pass arguments as a list — not delegate parsing to a system shell like Bash.
- **Built-in commands** (e.g. `cat`, `head`, `wc`, `echo`, `cd`) must be implemented using your own Python code. Do not simply call the equivalent external programs via `subprocess`. The purpose of these built-ins is for you to demonstrate your understanding of how these operations work at the programming level.
- You must **not** install any external dependencies beyond those already included in the starter template (`psutil` and `requests`). You are free to use any module from the Python standard library.
- Your shell must run on **Linux**. This is the target platform and the environment in which it will be tested. You are welcome to additionally support other operating systems (e.g. macOS, Windows), but Linux compatibility is required.

## Specification

### Part 1: Command Execution & Built-in Commands [25%]

The most basic function of a shell is to accept user input and execute programs. Your shell must parse user input, identify the command and its arguments, and execute it as a **child process** using Python's `os` and `subprocess` modules. Your shell should display an **informative prompt showing the current user, group, and current directory** and handle cases where a command is not found gracefully.

Your shell must handle **Ctrl+C (SIGINT)** so that it does _not_ terminate your shell but instead cancels the current input and shows a new prompt. This is provided in the starter template.

In addition to executing external programs, your shell must implement the following **built-in commands** natively (i.e. handled by your shell's own code, not by calling external programs):

- **`cd <path>`:** change the current working directory
- **`pwd`:** print the current working directory
- **`echo <text>`:** print text to the terminal
- **`exit`:** terminate the shell cleanly
- **`help`:** display a list of available built-in commands with brief descriptions
- **`procinfo <pid>`:** use Python's `os` or `psutil` module to display information about a process: its status, memory usage, CPU time, and parent PID

### Part 2: File Utilities [15%]

A practical shell should be able to work with files directly. Implement the following file operation commands as **built-ins using Python's file I/O**. Do not simply call the equivalent external programs via `subprocess`. The goal is for you to build your own to demonstrate your understanding of how file operations work at the programming level.

Your shell must support:

- **`cat <file> [file2 ...]`:** read and display the contents of one or more files. Handle missing files with a clear error message.
- **`head [-n N] <file>`:** display the first _N_ lines of a file (default: 10)
- **`wc <file> [file2 ...]`:** count and display the number of lines, words, and characters in one or more files. Display totals when multiple files are given.

Each command should handle errors gracefully (e.g. file not found, permission denied).

### Part 3: Memory & System Monitoring [15%]

Implement a built-in command called **`sysinfo`** that provides a real-time view of the system's resource usage, similar to `top` or `htop`. This command should display:

- **Memory usage:** total, used, available, and percentage of physical memory in use. Also show swap memory usage.
- **CPU usage:** overall CPU usage percentage and per-core breakdown
- **Top processes:** display the top 10 processes sorted by memory or CPU usage. Use a `--sort` flag to specify the order (e.g. `sysinfo --sort cpu` or `sysinfo --sort memory`). Default to sorting by memory.
- **Refreshing display:** the output should refresh at a configurable interval (default: every 2 seconds).

Use the `psutil` library to access system information. In your report, explain the difference between physical and virtual memory, and how the operating system uses paging and swap space. Relate this to what your `sysinfo` command displays.

### Part 4: Concurrency - Multi-threaded File Downloader [20%]

To demonstrate your understanding of threads and concurrency, implement a built-in command called **`download`** that downloads files from the internet using a **producer-consumer** pattern. This command should:

- Maintain a **shared queue** of URLs to download
- Run a **pool of worker threads** that consume URLs from the queue and download them
- Use a **thread-safe counter** (protected by a lock) to track the number of completed downloads
- **`download <file>`:** read a text file containing URLs (one per line), add them to the download queue, and immediately begin downloading with 3 worker threads. A sample file `test_urls.txt` is provided for testing.
- **`download <file> -w <number>`:** same as above, but with a custom number of worker threads (e.g. `download urls.txt -w 5`)
- **`download --status`:** show the current state of the download queue and workers (how many items queued, how many workers active, completed count)
- Downloaded files should be saved to a **`downloads`** folder in the current working directory. If the folder does not exist, your shell should create it automatically.
- Handle errors gracefully. An invalid URL or network timeout should not crash the worker thread or the shell

The worker threads should run in the background, allowing the user to continue using the shell and check progress with `download --status`.

### Part 5: Extra Mile [10%]

This is an opportunity for you to go beyond the specification and add one or more features that improve your shell. This could be:

- **Background processes (`&`):** when a command ends with `&`, run it in the background and immediately return the prompt to the user. Display the process ID (PID) when a background process starts.
- **I/O redirection:** support `>`, `>>`, and `<` to redirect command output and input to and from files
- **Pipes:** connect commands with `|` so the output of one feeds into the next
- **Tab completion:** auto-complete file paths and command names as the user types
- **Shell scripting:** support running script files with variables and control flow (`if`/`else`, `for` loops)
- **Aliases:** allow users to define command shortcuts (e.g. `alias ll="ls -la"`)
- **Colour and theming:** coloured output for different file types, custom prompt themes
- **Command chaining:** support `&&` (run next only if previous succeeds) and `||` (run next only if previous fails)

## Presentation and Documentation [15%]

### Demonstration

You will give a live demonstration of your shell on the **week of 27th April** showing your shell executing commands, working with files, downloading files concurrently, and displaying system information. Be prepared to answer questions about your implementation to demonstrate understanding of your work. **You must demo your project to receive a grade for it.**

### Report

Write a technical report of approximately **1,000–1,500 words** covering:

- **Architecture:** how you structured your shell (e.g. modules, functions, main loop) and why
- **File operations:** how your built-in file utilities work and how Python's file I/O maps to operating system concepts (file descriptors, system calls)
- **Process model:** how your shell creates and manages child processes. Explain how the Ctrl+C (SIGINT) handling in the starter template works and why it is necessary.
- **Concurrency:** your approach to multi-threading in the downloader, including the synchronisation primitives used and why. Explain how your thread-safe counter works and why a lock is needed.
- **Memory & OS concepts:** explanation of physical vs. virtual memory, paging, and how your `sysinfo` command relates to these concepts
- **Challenges and limitations:** what was difficult, what you would do differently, and any known limitations

Write for a technical audience who has already taken this course.

## Submission

The deadline for submission is **Sunday 3rd May at 23:59**. For each day that your assignment is submitted late, 5% will be deducted. Assignments submitted more than 7 days late will not be accepted. Academic integrity guidance for this project is available [on the course website](https://mcandru.github.io/architecture-and-operating-systems/academic-integrity).

You will be required to submit the following by **Sunday 3rd May**:

- **Your shell source code:** submit the link to a private GitHub repository containing your source code. Add the lecturer as a collaborator to the repository. Ensure that the repository includes a `README.md` complete with setup instructions and dependencies listed.
- **report.pdf:** the technical report as described above
