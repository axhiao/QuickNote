import os
from dotenv import load_dotenv

class Settings():
    
    def __init__(self) -> None:
        if load_dotenv is not None:
            load_dotenv()
        self.provider = os.getenv("PROVIDER", "").strip().lower()
        self.memos_base_url = os.getenv("MEMOS_BASE_URL", "https://note.zimu.info").rstrip("/")
        self.memos_token = os.getenv("MEMOS_TOKEN", "").strip()
        self.memos_user_id = int(os.getenv("MEMOS_USER_ID", "").strip())
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "").strip()
        self.openai_base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com").rstrip("/")
        self.openai_model = os.getenv("OPENAI_MODEL", "").strip()
        self.ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/")
        self.ollama_model = os.getenv("OLLAMA_MODEL", "").strip()
        
        # gemini
        self.gemini_api_key = os.getenv("GEMINI_API_KEY", "").strip()
        self.gemini_model   = os.getenv("GEMINI_MODEL", "").strip()
        
        sys_prompt = os.getenv(
            "SYSTEM_PROMPT",
            "You are a precise image analysis and transcription system. Inspect the image and extract the content relevant to the user request. Return only valid Markdown as the output.",
        ).strip()
        
        self.system_prompt = sys_prompt
        # Application
        self.app_version = os.getenv("APP_VERSION", "0.0.1").strip()
        self.app_name    = os.getenv("APP_NAME", "QuickNote Server").strip()
        self.environment = os.getenv("ENVIRONMENT", "dev").strip() 
        self.log_level   = os.getenv("LOG_LEVEL", "INFO").strip()
        

settings = Settings()
