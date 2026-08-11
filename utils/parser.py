import re

def normalize_command(command: str) -> str:
    return command.split(maxsplit=1)[0] if command else ""

def is_valid_command(command: str) -> bool:
    base = normalize_command(command)

    return (
        bool(re.match(r"^[a-zA-Z0-9._/+!-]+$", base))
        and base not in {"-", "..", ":", ":"}
    )
