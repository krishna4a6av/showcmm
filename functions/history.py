from pathlib import Path

from db.database import insert_commands_bulk
import utils.parser as parser
from utils.read_toml import get_shells

def list_available_shells() -> dict[str, dict]:
    shells = get_shells()

    return {
        name: config
        for name, config in shells.items()
        if Path(config["path"]).expanduser().exists()
    }


def choose_shells(available_shells: dict) -> dict:
    if not available_shells:
        raise ValueError("No history shell history files found.")

    selected = {}
    max_choice = len(available_shells)

    print("Available shell histories:")
    for i, shell in enumerate(available_shells, 1):
        print(f"{i}. {shell} "
        f"({Path(available_shells[shell]['path']).expanduser()})"
)
    print("0. All shells\n")

    try:
        choices = list(map(int, input("Choose a shell (number or multiple numbers separated by space): ").split()))
    except ValueError:
        raise ValueError("Enter valid no.")
    if 0 in choices:
        choices = list(range(1, max_choice + 1))

    elif not choices or max(choices) > max_choice or min(choices) < 0:
        raise RuntimeError("Invalid Choice.")

    for i, shell in enumerate(available_shells, 1):
        if i in choices:
            selected[shell] = available_shells[shell]

    return selected


def import_history(shell_config: dict) -> None:
    file_path = Path(shell_config["path"]).expanduser()
    parser_name = shell_config["parser"]

    if parser_name not in parser.PARSERS:
        raise ValueError(f"Unknown parser: {parser_name}")

    parse = parser.PARSERS[parser_name]

    batch = []

    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        for line in file:
            command = parse(line)

            if command and parser.is_valid_command(command):
                batch.append(command)

            if len(batch) >= 100:
                insert_commands_bulk(batch)
                batch = []

    if batch:
        insert_commands_bulk(batch)
