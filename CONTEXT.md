# PYSH project context

This file is a handoff for continuing Stage 2 work in a new chat. See [ROADMAP.md](ROADMAP.md) for the staged plan and [NOTES.md](NOTES.md) for Stage 1 learning notes.

## Current state

- `shell.py` reads one line at a time and uses `shlex.split()` for words and quotes.
- `cd`, `export`, and `exit` are builtins that run in the shell process.
- External commands use `os.fork()`, `os.execvp()`, and `os.waitpid()`. `run_external()` returns a decoded numeric exit status, but the main loop does not retain or display it yet.
- The Stage 1 Linux smoke check in `NOTES.md` is still pending. Stage 2 status and pipelines have not been implemented.

## Stage 2 goal and design discussed

1. Show the most recent command's exit code in the prompt.
2. Support a pipeline of two external commands, then any number of external commands using the same loop. A pipeline with N commands has N−1 pipe connections.
3. Use `shlex.shlex(line, posix=True, punctuation_chars="|")` with whitespace splitting and comments disabled to recognize `|` with or without surrounding spaces. Group the resulting tokens into a list of argument lists, one inner list per command. Reject empty segments and unsupported `||`.
4. Keep parsing separate from execution. A parser returns grouped commands; a pipeline runner starts all children, connects their standard streams, closes unused pipe ends, waits for every child, and returns a numeric status. A single command can continue through the existing command handler.
5. Do not call the current `run_external()` once per pipeline segment: it waits immediately after each fork, whereas pipeline children must be started before waiting.
6. `os.pipe()` supplies a read and write file descriptor. In children, `os.dup2()` connects the producer's standard output to the write end and the consumer's standard input to the read end before `execvp()`. The final command's standard output remains connected to the terminal.

## Proposed acceptance checks

- A successful command updates the next prompt to status `0`; a failing command shows its nonzero status, and PYSH remains open.
- `printf 'hello\n' | wc -l` prints `1`.
- `printf 'b\na\n' | sort | head -n 1` prints `a`.
- A pipeline reports the exit status of its last command and returns to the prompt, including when one command fails.
- Leading, trailing, or repeated pipe operators produce a clear parse error without terminating PYSH.
- All children are collected with `waitpid()` and unused pipe ends are closed so a reader can receive EOF.

## Open choices and known limitation

- A standalone quoted or escaped pipe (for example, `echo "|"`) becomes the same string token as an operator with this `shlex` approach. Correctly distinguishing them needs a parser that retains quote or escape context. This was accepted as a possible first-version limitation, not resolved.
- For an initial pipeline implementation, reject builtins inside pipelines with a clear error. `cd` and `export` change the shell process, so their pipeline semantics need a separate decision.
- Decide how builtin and parse-error statuses update the prompt when implementing status tracking.

## Collaboration preference

The user is designing and implementing PYSH to learn Unix process handling. Discuss concepts and review their approach; do not provide code snippets unless explicitly requested.
