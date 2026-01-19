import base64

import httpx

from app.config import get_settings
from app.providers.base import Provider


class OpenAIProvider(Provider):
    async def analyze_image(self, prompt: str, image_bytes: bytes, content_type: str) -> str:
        settings = get_settings()
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY is not set")
        if not settings.openai_model:
            raise ValueError("OPENAI_MODEL is not set")

        data_url = f"data:{content_type};base64,{base64.b64encode(image_bytes).decode('ascii')}"
        payload = {
            "model": settings.openai_model,
            "messages": [
                {
                    "role": "system",
                    "content": settings.system_prompt,
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": data_url}},
                    ],
                },
            ],
        }
        headers = {
            "Authorization": f"Bearer {settings.openai_api_key}",
            "Content-Type": "application/json",
        }
        async with httpx.AsyncClient(base_url=settings.openai_base_url, timeout=60) as client:
            response = await client.post("/v1/chat/completions", json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()

        return data["choices"][0]["message"]["content"]
