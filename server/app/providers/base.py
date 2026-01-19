from abc import ABC, abstractmethod
from typing import Any


class Provider(ABC):
    @abstractmethod
    async def analyze_image(self, prompt: str, image_bytes: bytes, content_type: str) -> str:
        raise NotImplementedError
