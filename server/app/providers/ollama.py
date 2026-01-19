import base64

import httpx

from app.config import get_settings
from app.providers.base import Provider


class OllamaProvider(Provider):
    async def analyze_image(self, prompt: str, image_bytes: bytes, content_type: str) -> str:
        settings = get_settings()
        if not settings.ollama_model:
            raise ValueError("OLLAMA_MODEL is not set")

        system_prompt = f"/no_think {settings.system_prompt}".strip()
        payload = {
            "model": settings.ollama_model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": prompt,
                    "images": [base64.b64encode(image_bytes).decode("ascii")],
                }
            ],
            "stream": False,
            "think":  False,
        }
        async with httpx.AsyncClient(base_url=settings.ollama_base_url, timeout=120) as client:
            response = await client.post("/api/chat", json=payload)
            response.raise_for_status()
            data = response.json()

        return data["message"]["content"]
