from app.providers.base import Provider


class UnimplementedProvider(Provider):
    def __init__(self, name: str) -> None:
        self._name = name

    async def analyze_image(self, prompt: str, image_bytes: bytes, content_type: str) -> str:
        raise NotImplementedError(f"Provider '{self._name}' is not implemented")
