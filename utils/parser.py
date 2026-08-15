import re

def normalize_command(command: str) -> str:
    return command.split(maxsplit=1)[0] if command else ""

def is_valid_command(command: str) -> bool:
    base = normalize_command(command)

    return (
        bool(re.match(r"^[a-zA-Z0-9._/+!-]+$", base))
        and base not in {"-", "..", ":", ":"}
    )

def parse_plain(line: str) -> str:
    return line.strip()


def parse_zsh(line: str) -> str:
    return ZSH_PATTERN.sub("", line.strip())


def parse_fish(line: str) -> str | None:
    prefix = "- cmd: "

    if not line.startswith(prefix):
        return None

    return line[len(prefix):].strip()

ZSH_PATTERN = re.compile(r"^: \d+:\d+;")

PARSERS = {
    "plain": parse_plain,
    "zsh": parse_zsh,
    "fish": parse_fish,
}
