from typing import Dict

from app.providers.base import Provider
from app.providers.ollama import OllamaProvider
from app.providers.openai import OpenAIProvider
from app.providers.unimplemented import UnimplementedProvider


class ProviderRegistry:
    def __init__(self) -> None:
        self._providers: Dict[str, Provider] = {
            "mock":   UnimplementedProvider("mock"),
            "ollama": OllamaProvider(),
            "openai": OpenAIProvider(),
            "gemini": UnimplementedProvider("gemini"),
            "claude": UnimplementedProvider("claude"),
        }

    def get(self, name: str) -> Provider:
        if name in self._providers:
            return self._providers[name]
        raise ValueError(f"Provider '{name}' not implemented")


registry = ProviderRegistry()
