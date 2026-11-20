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

    print(tokens)
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
           tokens = shlex.split(line,comments=False,posix=True)
        except(ValueError):
            print("value error in tokens if it happens fucking figure out was wrong wit it \n")
            continue
        if not tokens:
            continue

        if not handle_command(tokens):
            break


if __name__ == "__main__":
    main()
