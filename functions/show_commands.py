import db.database as db
import utils.parser as parser


def list_commands() ->  list[tuple[str, int]]:
    commands = db.get_all_commands()
    if not commands:
        raise ValueError("No commands found in the database.")

    summary = {}
    for cmd, count in commands:
        key = parser.normalize_command(cmd)
        if parser.is_valid_command(key):
            summary[key] = summary.get(key, 0) + count
    grouped = sorted(summary.items(), key=lambda x: x[0])

    return grouped


def top_commands(limit: int) ->  list[tuple[str, int]]:
    commands = db.get_all_commands()
    if not commands:
        raise ValueError("No commands found in the database.")

    summary = {}
    for cmd, count in commands:
        key = parser.normalize_command(cmd)
        if parser.is_valid_command(key):
            summary[key] = summary.get(key, 0) + count

    grouped = sorted(summary.items(), key=lambda x: x[1], reverse=True)
    return grouped[:limit]


def show_filtered_commands(query: str, limit: int) ->  list[tuple[str, int]]:
    if not query:
        raise ValueError("No filter provided.")

    commands = db.get_filter_commands(query)
    if not commands:
        raise ValueError("No command found")

    return commands[:limit]
