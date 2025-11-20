import json
import pathlib

from typing import Any


def read_json_file(path: pathlib.Path) -> Any:
    if not path.is_file():
        raise FileNotFoundError(path)

    content_text = path.read_text(encoding="utf-8")
    content_json = json.loads(content_text)

    return content_json
