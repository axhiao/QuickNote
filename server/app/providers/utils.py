import json
from typing import Any, Dict


def extract_json(content: str) -> Dict[str, Any]:
    content = content.strip()
    if content.startswith("```"):
        lines = [line for line in content.splitlines() if not line.strip().startswith("```")]
        content = "\n".join(lines).strip()
    try:
        return json.loads(content)
    except json.JSONDecodeError as exc:
        raise ValueError("LLM response is not valid JSON") from exc
