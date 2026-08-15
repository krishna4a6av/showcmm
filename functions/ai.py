import os
import config
from openai import OpenAI
from utils.json_data import commands_in_json

def analyze(mode: str) -> str:
    api_key = os.environ.get("API_KEY")

    if api_key == None:
        raise RuntimeError("No API_KEY in .env")

    messages = []

    prompts = {
            "roast": config.roast_prompt,
            "learn": config.learn_prompt,
            "workflow": config.workflow_prompt,
            "level": config.level_prompt,
            "alias": config.alias_prompt,
            }

    client = OpenAI(base_url=config.BASE_URL, api_key=api_key,)

    if mode not in prompts:
        raise ValueError(f"Unknown analysis mode: {mode}")

    messages.append({ "role": "system", "content": prompts[mode] })
    messages.append({ "role": "user", "content": commands_in_json()})

    try:
        response = client.chat.completions.create(
                model=config.MODEL,
                messages=messages,
                )
    except Exception as e:
        raise RuntimeError(f"Failed to contact AI provider: {e}")

    content = response.choices[0].message.content

    if not content:
        raise ValueError("Model returned an empty response.")

    return content
