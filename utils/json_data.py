import json
import db.database as db
import utils.parser as parser


def commands_in_json() -> str:
    commands = db.get_all_commands()

    frequency = {}

    for command, count in commands:
        base = parser.normalize_command(command)

        if parser.is_valid_command(base):
            frequency[base] = frequency.get(base, 0) + count

    data = {
        "total_commands": sum(frequency.values()),
        "unique_commands": len(frequency),
        "commands": dict(
            sorted(
                frequency.items(),
                key=lambda item: item[1],
                reverse=True
            )
        )
    }

    return json.dumps(data, indent=2)


# Dumps whole history to AI. change call in functions/ai.
# Provides more personalized AI responses but has privacy risks as it may include sensitive data from your command history.
# Use only with a local LLM or a provider you trust. currently not used.
def full_commands_in_json():
    commands = db.get_all_commands()
    json_commands = json.dumps(commands, indent=2)
    print(json_commands)
