from __future__ import annotations
from typing import Any
from google import genai
from google.genai import types

from config import load_config
from prompts import SYSTEM_PROMPT

config = load_config()
api_key = config.get("GOOGLE_API_KEY")
model = config.get("GOOGLE_MODEL")

client = genai.Client(api_key=api_key)
config = types.GenerateContentConfig(
    system_instruction=SYSTEM_PROMPT
)


def build_contents(messages: list[dict[str, str]]) -> list[dict[str, Any]]:
    contents: list[dict[str, Any]] = []

    for msg in messages:
        role = "user" if msg["role"] == "user" else "model"
        contents.append(
            {
                "role": role,
                "parts": [{"text": msg["content"]}],
            }
        )

    return contents


def stream_response(messages: list[dict[str, str]]) -> Any:
    contents = build_contents(messages)
    return client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=config,
    )
