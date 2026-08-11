import db.database as db
import utils.parser as parser
import utils.display as display


def list_commands() -> None:
    commands = db.get_all_commands()
    if not commands:
        raise ValueError("No commands found in the database.")

    summary = {}
    for cmd, count in commands:
        key = parser.normalize_command(cmd)
        if parser.is_valid_command(key):
            summary[key] = summary.get(key, 0) + count
    grouped = sorted(summary.items(), key=lambda x: x[0])

    display.display_table(grouped)


def top_commands(limit: int) -> None:
    commands = db.get_all_commands()
    if not commands:
        raise ValueError("No commands found in the database.")

    summary = {}
    for cmd, count in commands:
        key = parser.normalize_command(cmd)
        if parser.is_valid_command(key):
            summary[key] = summary.get(key, 0) + count

    grouped = sorted(summary.items(), key=lambda x: x[1], reverse=True)
    display.display_table(grouped[:limit])


def show_filtered_commands(query: str) -> None:
    if not query:
        raise ValueError("No filter provided.")

    commands = db.get_filter_commands(query)
    if not commands:
        raise ValueError("No command found")

    display.display_table(commands)
