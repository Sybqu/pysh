# PYSH roadmap

This is a provisional learning plan. PYSH uses Python's standard library and starts with Unix process primitives.

## Stage 1 — single commands

- Prompt and read one line at a time; parse words with `shlex`.
- Run external commands with `fork`, `execvp`, and `waitpid`.
- Handle `cd` and `exit` in the shell process; handle blank lines and EOF.
- Current code also supports `export`. Implementation is in place; a Linux smoke test is pending.

## Stage 2 — status and pipes

- Show the last exit code in the prompt.
- Connect two commands with `os.pipe()` and `os.dup2()`, then support pipelines of any length.

## Stage 3 — shell operators and environment

- Add input and output redirection with `<`, `>`, and `>>`.
- Expand `$VAR`, and use exported values from `os.environ`.
- Add `&&` and `;` command control.

## Stage 4 — stretch work

- Keep PYSH alive when Ctrl-C interrupts a running child.
- Support background jobs with `&` and a `jobs` builtin.
- Compare the fork/exec implementation with `subprocess.Popen`.
- Add interactive command history with `readline`.
