import tomllib
from pathlib import Path

CONFIG_DIR = Path.home() / ".config" / "showcmm"
CONFIG_FILE = CONFIG_DIR / "config.toml"

DEFAULT_CONFIG = """\
[shells.bash]
path = "~/.bash_history"
parser = "plain"

[shells.zsh]
path = "~/.zsh_history"
parser = "zsh"

[shells.fish]
path = "~/.local/share/fish/fish_history"
parser = "fish"
"""


def create_default_config() -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(DEFAULT_CONFIG)


def get_shells() -> dict[str, dict]:
    if not CONFIG_FILE.exists():
        create_default_config()

    with CONFIG_FILE.open("rb") as file:
        data = tomllib.load(file)

    return data.get("shells", {})
