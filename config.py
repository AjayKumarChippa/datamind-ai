import json
import os
from pathlib import Path
from typing import Any


CONFIG_PATH = Path(__file__).with_name("config.json")


def load_config(path: str | Path | None = None) -> dict:
    resolved_path = Path(path or CONFIG_PATH)

    with resolved_path.open("r", encoding="utf-8") as file:
        return json.load(file)


config = load_config()

api_key = os.getenv("GOOGLE_API_KEY")
model = config.get("GOOGLE_MODEL")