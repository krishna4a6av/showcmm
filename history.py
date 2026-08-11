import os
import re
from pathlib import Path

from db.database import insert_commands_bulk
from functions import show_commands
import utils.parser as parser


def list_available_shells() -> dict:
    zdotdir = os.environ.get("ZDOTDIR")

    shells = {
        "bash": Path(os.path.expanduser("~/.bash_history")),
        "zsh": Path(f"{zdotdir}/.zsh_history" if zdotdir else os.path.expanduser("~/.zsh_history")),
        "fish": Path(os.path.expanduser("~/.local/share/fish/fish_history")),
    }
    return {shell: path for shell, path in shells.items() if os.path.exists(path)}

def choose_shells() -> list:
    available_shells = list_available_shells()
    if not available_shells:
        raise ValueError("No history shell history files found.")

    print("Available shell histories:")
    for i, shell in enumerate(available_shells, 1):
        print(f"{i}. {shell} ({available_shells[shell]})")
    print("0. All shells")

    choice = input("Choose a shell (number or multiple numbers separated by space): ").strip()
    if choice == "0":
        return list(available_shells.values())

    try:
        choices = [int(c) - 1 for c in choice.split()]
        paths = list(available_shells.values())
        return [paths[c] for c in choices if 0 <= c < len(paths)]
    except (ValueError, IndexError):
        raise ValueError("Invalid choice.")

def read_history() -> None:
    shell_type = os.environ.get("SHELL", "Unknown")
    print(f"Detected Shell: {shell_type}")

    history_files = choose_shells()

    batch = []
    batch_size = 100

    for file_path in history_files:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
            for line in file:
                command = re.sub(r"^: \d+:\d+;", "", line.strip())
                if parser.is_valid_command(command):
                    batch.append(command)

                if len(batch) >= batch_size:
                    insert_commands_bulk(batch)
                    batch = []

    if batch:
        insert_commands_bulk(batch)
