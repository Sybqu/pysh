import os
import sys
import shlex


def cd(path: str) -> None:
    if not os.path.exists(path):
        print("No such file or directory!")
    elif not os.path.isdir(path):
        print("Thats a file :3")
    else:
        try:
            os.chdir(path)
        except OSError as error:
            print(f"cd: {error}")


def export(assignments: list[str]) -> None:
    if not assignments:
        print("shii looks like u forgot an arg again")
        return

    for assignment in assignments:
        if "=" not in assignment:
            print(f"export: expected NAME=value, got {assignment!r}")
            continue

        name, value = assignment.split("=", 1)
        if not name:
            print("export: missing variable name")
            continue

        os.environ[name] = value


def run_external(command: str, tokens: list[str]) -> int:
    # Flush before fork so buffered output is not copied into the child.
    sys.stdout.flush()
    sys.stderr.flush()
    try:
        pid = os.fork()
    except OSError as error:
        # Fork raised an exception, so there is no pid to use after this point.
        print(f"pysh: fork: {error}", file=sys.stderr)
        return 1

    if pid > 0:
        # The parent got the child's real PID; waitpid collects that child.
        _, wait_status = os.waitpid(pid, 0)
        return os.waitstatus_to_exitcode(wait_status)

    try:
        # pid == 0 marks this branch as the child; exec replaces this process.
        os.execvp(command, tokens)
    except OSError as error:
        # Only an exec failure gets here. End the child, not the shell parent.
        print(f"pysh: {command}: {error.strerror or error}", file=sys.stderr, flush=True)
        os._exit(127 if isinstance(error, FileNotFoundError) else 126)


def handle_command(tokens: list[str]) -> bool:
    command, *args = tokens

    if command == "cd":
        if not args:
            print("Perhaps u forgot the argument?")
        else:
            cd(args[0])
    elif command == "export":
        export(args)
    elif command == "exit":
        print("okie bye bye have a nice day!")
        return False
    else:
        # A command's exit status is not the bool that controls PYSH's loop.
        run_external(command, tokens)

    return True


def main() -> None:
    print("Welcome to PYSH \n")
    while True:
        sys.stdout.write(f"{os.getcwd()}$ ")
        sys.stdout.flush()

        line = sys.stdin.readline()
        if line == "":
            break

        try:
            tokens = shlex.split(line, comments=False, posix=True)
        except ValueError as error:
            print(f"pysh: parse: {error}", file=sys.stderr)
            continue
        if not tokens:
            continue

        if not handle_command(tokens):
            break


if __name__ == "__main__":
    main()
