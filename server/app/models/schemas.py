from typing import Optional

from pydantic import BaseModel, Field


class ImageJsonRequest(BaseModel):
    image_base64: str = Field(..., description="Base64 encoded image bytes") # check， field required
    prompt: str
    upload_to_memos: bool = False
    provider: Optional[str] = None
    filename: Optional[str] = None
    content_type: Optional[str] = None

class LLMResult(BaseModel):
    markdown: str


class MemosAttachment(BaseModel):
    name: str
    filename: str
    content_type: str


class MemosResult(BaseModel):
    memo_name: Optional[str] = None
    attachment: Optional[MemosAttachment] = None


class ImageResponse(BaseModel):
    llm: LLMResult
    memos: Optional[MemosResult] = None
