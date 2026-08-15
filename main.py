import argparse
import os
from dotenv import load_dotenv

from functions import history, show_commands, delete
from functions import ai as ai_module
import utils.display as display

def handle_update() -> None:
    confirm = input(
        "Clear saved command history before importing? "
        "(not doing so will lead to existing and new commands being appended)"
    )

    if confirm.lower() not in {"y", "yes"}:
        print("Cancelled")
        return

    try:
        delete.delete_database()
        print("Database removed successfully.")
    except ValueError as e:
        print(f"Error: {e}")

    try:
        shell_type = os.environ.get("SHELL", "Unknown")
        print(f"Detected Shell: {shell_type}\n")

        available_shells = history.list_available_shells()
        selected_shells = history.choose_shells(available_shells)

        for shell_config in selected_shells.values():
            history.import_history(shell_config)

        print("History added successfully.")

    except ValueError as e:
        print(f"Error: {e}")



def handle_view(args) -> None:
    try:
        if args.top:
            display.display_table(show_commands.top_commands(args.limit))

        elif args.all:
            display.display_table(show_commands.list_commands())

        elif args.filter:
            display.display_table(show_commands.show_filtered_commands(args.filter, args.limit))

        else:
            display.display_table(show_commands.top_commands(args.limit))
    except ValueError as e:
        print(f"Error: {e}")


def handle_delete() -> None:
    confirm = input("Delete all command history (only the `showcmm` history will be removed)?")
    if confirm.lower() in {"y", "yes"}:
        try:
            delete.delete_database()
            print("Database removed sucessfully")
        except ValueError as e:
            print(f"Error: {e}")
    else:
        print("Cancelled.")


def handle_ai(args) -> None:
    try:
        print(ai_module.analyze(args.mode))
    except Exception as e:
        print(f"Error: {e}")


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(prog="showcmm", description="Track and analyze your shell command usage.")
    subparsers = parser.add_subparsers(dest="command")

    view = subparsers.add_parser("view", help="Display command statistics")
    view.add_argument("-t", "--top", action="store_true", help="Show top commands")
    view.add_argument("-a", "--all", action="store_true", help="Show all commands")
    view.add_argument("-f", "--filter", metavar="QUERY", help="Filter commands")
    view.add_argument("-l","--limit", type=int, default=10, help="Number of commands to display")
    subparsers.add_parser("update", help="Import shell history")
    subparsers.add_parser("delete", help="Delete the database")
    ai = subparsers.add_parser("ai", help="Use ai to learn or roast")
    ai.add_argument("--roast", dest="mode", action="store_const", const="roast", help="roast based on top commands")
    ai.add_argument("--learn", dest="mode", action="store_const", const="learn", help="recommends more prodoctive commands")
    ai.add_argument("--workflow", dest="mode", action="store_const", const="workflow", help="hallucinate some misinformation")
    ai.add_argument("--level", dest="mode", action="store_const", const="level", help="hallucinate some misinformation")
    ai.add_argument("--alias", dest="mode", action="store_const", const="alias", help="hallucinate some misinformation")

    args = parser.parse_args()

    match args.command:
        case "update":
            handle_update()
        case "view":
            handle_view(args)
        case "delete":
            handle_delete()
        case "ai":
            handle_ai(args)


if __name__ == "__main__":
    main()
