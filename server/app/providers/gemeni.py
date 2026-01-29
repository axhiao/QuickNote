from google import genai
from google.genai import types
import base64
import logging
import httpx

from app.config import settings
from app.providers.base import Provider

logger = logging.getLogger(__name__)

class GeminiProvider(Provider):
    
    def __init__(self):
        super().__init__()
        self.client = genai.Client(api_key=settings.gemini_api_key)
        
    async def analyze_image(self, prompt: str, image_bytes: bytes, content_type: str, tags: list[str]) -> str:
        if not settings.gemini_api_key:
            raise ValueError("GEMINI_API_KEY is not set")
        if not settings.gemini_model:
            raise ValueError("GEMINI_MODEL is not set")
        
        response = self.client.models.generate_content(
            model=settings.gemini_model,
            contents=[
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type=content_type,
                ),
                prompt
            ],
            # set System Prompt
            config=types.GenerateContentConfig(
                system_instruction=settings.system_prompt.format(hashtags=",".join(tags)),
                temperature=0.7,
            )
        )
        return response.text
