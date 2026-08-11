import argparse

from functions import history
from functions import show_commands
from db.database import delete_database

def handle_update() -> None:
    confirm = input("Clear saved command history before importing? (not doing so will lead to existing and new commands being appended)")
    if confirm.lower() in {"y", "yes"}:
        cleared = delete_database()
        if cleared:
            print("Database removed successfully.")
        else:
            print("No datatbase file exists")

    try:
        history.read_history()
        print("History added sucessfully.")
    except ValueError as e:
        print(f"{e}")

def handle_view(args) -> None:
    try:
        if args.top:
            show_commands.top_commands(args.limit)
        elif args.all:
            show_commands.list_commands()
        elif args.filter:
            show_commands.show_filtered_commands(args.filter)
        else:
            show_commands.top_commands(10)
    except ValueError as e:
        print(f"{e}")

def handle_delete() -> None:
    confirm = input("Delete all command history (only the `showcmm` history will be removed)?")
    if confirm.lower() in {"y", "yes"}:
        cleared = delete_database()
        if cleared:
            print("Database removed sucessfully")
        else:
            print("No db file exists")
    else:
        print("Cancelled.")



def main():
    parser = argparse.ArgumentParser(prog="showcmm", description="Track and analyze your shell command usage.")
    subparsers = parser.add_subparsers(dest="command")

    view = subparsers.add_parser("view", help="Display command statistics")
    view.add_argument("--top", action="store_true", help="Show top commands")
    view.add_argument("--all", action="store_true", help="Show all commands")
    view.add_argument("--filter", metavar="QUERY", help="Filter commands")
    view.add_argument("--limit", type=int, default=10, help="Number of commands to display")
    subparsers.add_parser("update", help="Import shell history")
    subparsers.add_parser("delete", help="Delete the database")

    args = parser.parse_args()

    match args.command:
        case "update":
            handle_update()
        case "view":
            handle_view(args)
        case "delete":
            handle_delete()


if __name__ == "__main__":
    main()
