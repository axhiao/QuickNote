import base64
import logging
from typing import Optional

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.config import settings
from app.memos.client import MemosClient
from app.providers.registry import registry
from app.models.schemas import ImageResponse, LLMResult, MemosResult

logger = logging.getLogger(__name__)

router = APIRouter()

def _provider_name(provider_override: Optional[str]) -> str:
    """
    Get the provider name, either from remote request or from .env settings.
    """
    provider = (provider_override or settings.provider).strip().lower()
    if not provider:
        raise HTTPException(status_code=400, detail="PROVIDER is not set")
    return provider

async def _llm_analyze_image(
    prompt: str,
    image_bytes: bytes,
    content_type: str,
    provider_override: Optional[str],
    tags: list[str],
) -> LLMResult:
    provider_name = _provider_name(provider_override)
    try:
        provider = registry.get(provider_name)
        data = await provider.analyze_image(prompt, image_bytes, content_type, tags)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    
    return LLMResult(markdown=data)


async def _upload_to_memos(
    client: MemosClient,
    prompt: str,
    llm: LLMResult,
    image_bytes: bytes,
    content_type: str,
    filename: str,
    imgbool: bool,
) -> Optional[MemosResult]:
    
    # create memo
    memo_name = await client.create_memo(llm.markdown)
    if not memo_name:
        raise HTTPException(status_code=502, detail="Failed to create memo")
    
    # upload img if user enables to do it.
    if imgbool:
        attachment = await client.upload_attachment(image_bytes, filename, content_type)
        await client.set_memo_attachments(memo_name, attachment.name, filename, content_type)
    
    
    return MemosResult(memo_name=memo_name, attachment=attachment)


@router.post("/v1/image", response_model=ImageResponse, description="Parse image data from form-data")
async def parse_image_data(
    image: UploadFile = File(...),
    prompt: str = Form(...),
    imgbool: bool = Form(False),
    provider: Optional[str] = Form(None),
):
    image_bytes = await image.read()
    if not image_bytes:
        raise HTTPException(status_code=400, detail="Empty image file")
    
    content_type = image.content_type
    client = MemosClient(
        settings.memos_base_url,
        settings.memos_token, 
        settings.memos_user_id
    )
    tags = await client.user_tags()
    tags = [key for key in tags.keys()]
    
    # call llm
    llm = await _llm_analyze_image(
        prompt, 
        image_bytes, 
        content_type, 
        provider, 
        tags
    )
    # store to memos
    memos = await _upload_to_memos(
        client,
        prompt,
        llm,
        image_bytes,
        content_type,
        image.filename,
        imgbool,
    )
    return ImageResponse(llm=llm, memos=memos)

