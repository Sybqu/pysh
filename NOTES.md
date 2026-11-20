# PYSH review notes

## Concepts to remember

- `stdin` is a stream. `readline()` gets one command line; an empty string means EOF, while a blank Enter gives a newline.
- `shlex.split()` turns a line into words while respecting quotes. It can raise `ValueError` for an unclosed quote; it does not execute operators.
- Arguments are a flat list: the shell chooses the program, while that program interprets its options and paths.
- `cd`, `exit`, and `export` run in the shell process. `os.environ` holds exported values for this process and future children.
- `fork()` creates a child with its own real PID. It returns `0` in that child and the child's PID in the parent; failure raises `OSError`.
- `execvp(file, argv)` searches `PATH` and replaces the existing child without creating another process. Its argument list starts with the program name. Success never returns.
- `waitpid(child_pid, 0)` makes the parent wait for that child and collect its status. It returns a PID and an encoded status; decode the status with `waitstatus_to_exitcode()`.
- Exit status `0` means success. An external command's status and the decision to keep PYSH open are different things.

## Mistakes and fixes so far

| Mistake | Fix or lesson |
| --- | --- |
| Iterating over all of `stdin` before printing tokens | Read one line per prompt; iteration continues until EOF. |
| Referring to `sys.stdout.flush` without calling it | Call the method so the prompt appears before input. |
| Testing the last character for an empty string | Compare the entire raw line with the empty string to detect EOF. |
| Comparing a token list with an empty string | Check whether the list is empty before reading its first item. |
| Using `is` for the `cd` command and referring to `os.path.isdir` without a path | Compare string values with equality and call the path check with the path. |
| Hiding a missing `cd` argument with a broad exception | Handle the missing argument specifically and keep other errors visible. |
| Using `str.split()` for quoted arguments | Use `shlex.split()`; an unclosed quote is input to report, then move to the next prompt. |
| Calling `line.shlex.split(...)` and reusing old tokens after a parse error | Call the module's splitter on the line; continue the loop after `ValueError`. |
| Splitting an export assignment at every `=` | Split at the first `=` so the value may contain more `=` characters. |
| Treating fork failure as a negative PID | Catch `OSError`; a failed fork gives no usable PID. |
| Using `pass` after fork failed | Report the error and return before trying to read an undefined PID. |
| Letting the parent reach `execvp` | Parent waits and returns; only the child reaches exec. |
| Passing separate words to `execvp` | Pass one complete argument list, as the current code now does. |
| Treating `waitpid`'s status as a plain exit code | The current code now decodes it with `waitstatus_to_exitcode()`. |
| Ending a forked child with normal Python cleanup | The current child error path now uses `os._exit()`. |
| Using a command's success status as the shell's keep-running flag | Keep the command's numeric status separate; only the `exit` builtin stops the prompt loop. |
| Printing a generic exec error just before `_exit()` | Include the actual `OSError` and flush stderr so the message is visible. |

## Design pivots

- Changed from command/option/path categories to a flat argument list; operators will need their own parsing later.
- Changed from manual whitespace splitting to `shlex` to focus on Python and Unix process behavior.
- Chose Linux for the fork/exec stages because native Windows Python has no `os.fork()`.
- Kept three builtins as direct dispatch checks; a lookup table can wait until there are more commands.
- Kept the low-level fork/exec route to learn Unix processes. `subprocess` remains the practical high-level tool for ordinary Python programs.

## Current state and next checks

1. External commands now fork, exec in the child, wait in the parent, and return a decoded numeric status. The shell loop keeps running after either success or failure.
2. Run `ls`, a missing command, and a command with a nonzero exit status on Linux before adding pipes or redirection. This Windows host has WSL but no installed Linux distribution.
3. Store the most recent command status when implementing `&&` and other control operators; the current dispatcher does not need it yet.
