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

## Avalible commands: 

| Command                       | Description                    |
| ----------------------------- | ------------------------------ |
| `showcmm view`                | Show top 10 commands           |
| `showcmm view --top`          | Show top commands              |
| `showcmm view --all`          | Show all commands              |
| `showcmm view --filter QUERY` | Filter commands                |
| `showcmm update`              | Import shell history           |
| `showcmm delete`              | Delete command history         |
| `showcmm ai --roast`          | Roast your command-line habits |
| `showcmm ai --learn`          | Suggest things to learn        |
| `showcmm ai --workflow`       | Analyze your workflows         |
| `showcmm ai --level`          | Assess your CLI skill level    |
| `showcmm ai --alias`          | Suggest useful aliases         |


## Configuration, Models & Prompts

AI configuration is defined in `config.py`.

You can change the AI provider, model, and prompts to suit your preferences.

### Model Configuration

By default, `showcmm` uses OpenRouter's free model routing:

```python
MODEL = "openrouter/free"
BASE_URL = "https://openrouter.ai/api/v1"
```
You can change MODEL to any model supported by your chosen OpenAI-compatible provider and update BASE_URL accordingly. For example:
```
MODEL = "your-model"
BASE_URL = "https://your-provider.example.com/v1"
```

Or A local model as follow:
```
MODEL = "your-local-model"
BASE_URL = "http://localhost:1234/v1"
```

### API_KEY
The API key is loaded from a .env file:

```
API_KEY=your_api_key
```

AI features are optional; command tracking and local statistics do not require an AI API key.

### Adding Another Shell

Shell configuration is stored at:

```
~/.config/showcmm/config.toml
````

Add another shell to config.toml and specify the parser that matches its history format.

- Available Parsers

| Parser  | Description                                                  |
| ------- | ------------------------------------------------------------ |
| `plain` | Simple line-by-line parsing, suitable for Bash-style history |
| `zsh`   | Parses Zsh history timestamps                                |
| `fish`  | Parses Fish history files                                    |

For example:
```
[shells.myshell]
path = "~/.myshell_history"
parser = "plain"
```

If none of the existing parsers work for your shell, you can add your own parsing logic in:
```
utils/parser.py
```


## License

This project is licensed under the [MIT License](LICENSE).



Please feel free to clone/fork this simple proj and adding your twists :)
