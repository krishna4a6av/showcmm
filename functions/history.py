import os
import re
from pathlib import Path

from db.database import insert_commands_bulk
import utils.parser as parser

ZSH_PATTERN = re.compile(r"^: \d+:\d+;")

def list_available_shells() -> dict:
    zdotdir = os.environ.get("ZDOTDIR")

    shells = {
        "bash": Path(os.path.expanduser("~/.bash_history")),
        "zsh": Path(f"{zdotdir}/.zsh_history" if zdotdir else os.path.expanduser("~/.zsh_history")),
        "fish": Path(os.path.expanduser("~/.local/share/fish/fish_history")),
    }
    return {shell: path for shell, path in shells.items() if os.path.exists(path)}


def choose_shells(available_shells: dict) -> dict:
    selected = {}
    max_choice = len(available_shells)

    print("Available shell histories:")
    for i, shell in enumerate(available_shells, 1):
        print(f"{i}. {shell} ({available_shells[shell]})")
    print("0. All shells\n")

    try:
        choices = list(map(int, input("Choose a shell (number or multiple numbers separated by space): ").split()))
    except ValueError:
        raise ValueError("Enter valid no.")
    if 0 in choices:
        choices = list(range(1, max_choice + 1))

    elif not choices or max(choices) > max_choice or min(choices) < 0:
        raise ValueError("Invalid Choice.")

    for i, shell in enumerate(available_shells, 1):
        if i in choices:
            selected[shell] = available_shells[shell]

    return selected


def import_history(shell_name: str, file_path: Path) -> None:
    batch = []
    batch_size = 100

    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        for line in file:
            command = ""
            if shell_name == "fish":
                prefix = "- cmd: "
                if not line.startswith(prefix):
                    continue

                command = line[len(prefix):].strip()
            else:
                command = ZSH_PATTERN.sub("", line.strip())

            if command and parser.is_valid_command(command):
                batch.append(command)

            if len(batch) >= batch_size:
                insert_commands_bulk(batch)
                batch = []
    if batch:
        insert_commands_bulk(batch)



def read_history() -> None:
    shell_type = os.environ.get("SHELL", "Unknown")
    print(f"Detected Shell: {shell_type}\n")

    available_shells = list_available_shells()
    if not available_shells:
        raise ValueError("No history shell history files found.")

    history_files = choose_shells(available_shells)

    for shell, file_path in history_files.items():
        import_history(shell, file_path)
