import os
from functools import lru_cache

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - optional dependency
    load_dotenv = None


class Settings:
    def __init__(self) -> None:
        if load_dotenv is not None:
            load_dotenv()
        self.provider = os.getenv("PROVIDER", "").strip().lower()
        self.memos_base_url = os.getenv("MEMOS_BASE_URL", "https://note.zimu.info").rstrip("/")
        self.memos_token = os.getenv("MEMOS_TOKEN", "").strip()
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "").strip()
        self.openai_base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com").rstrip("/")
        self.openai_model = os.getenv("OPENAI_MODEL", "").strip()
        self.ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/")
        self.ollama_model = os.getenv("OLLAMA_MODEL", "").strip()
        
        sys_prompt = os.getenv(
            "SYSTEM_PROMPT",
            "You are a precise image analysis and transcription system. Inspect the image and extract the key content relevant to the user's request.",
        ).strip()
        self.system_prompt = sys_prompt
        


@lru_cache
def get_settings() -> Settings:
    return Settings()
