# showcmm

**showcmm** is a command-line tool for tracking, analyzing, and understanding your shell usage.

It imports command history from your shell, stores command statistics locally in SQLite, and provides a simple CLI for exploring your habits. It can also optionally use AI to analyze your command-line habits, roast your workflow, and suggest improvements.

> Built primarily as a personal project to explore Python, SQLite, CLI tooling, shell history parsing, and AI integration.

# Setup

Clone the repo and run the setup script:

```bash
git clone https://github.com/krishna4a6av/command_tracker.git
cd command_tracker
chmod +x setup.sh
./setup.sh
```

To remove:
```bash
cd command_tracker
chmod +x uninstall.sh
./uninstall.sh
```

## Features

- Track shell command usage with SQLite
- View your most-used commands
- View all tracked commands
- Filter commands
- Import history from multiple shells
- Configurable shell history paths and parsers
- AI-powered command-line analysis
- AI modes for:
  - `roast` — roast your habits
  - `learn` — suggest things to learn
  - `workflow` — identify workflow improvements
  - `level` — estimate your command-line skill level
  - `alias` — suggest useful aliases
- Man page
- Local SQLite database


## Adding Another Shell

The shell configuration is stored at:

```text
~/.config/showcmm/config.toml
```
Add other shell in the config.toml with the parser that suits the file.
'plain': simple line-by-line parsing, suitable for Bash-style history
'zsh': parses Zsh history timestamps
'fish': parses Fish history files

example toml:
```
[shells.myshell]
path = "~/.myshell_history"
parser = "plain"
```

- Add your own parsing logic for different shell in "utils/parser.py".

## License

This project is licensed under the [MIT License](LICENSE).



Please feel free to clone/fork this simple proj and adding your twists :)
