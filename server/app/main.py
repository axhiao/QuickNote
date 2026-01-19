import base64
from typing import Optional

from fastapi import FastAPI, File, Form, HTTPException, UploadFile

from app.config import get_settings
from app.memos.client import MemosClient
from app.providers.registry import registry
from app.schemas import ImageJsonRequest, ImageResponse, LLMResult, MemosResult

app = FastAPI(title="QuickNote Server")


def _get_provider_name(provider_override: Optional[str]) -> str:
    provider = (provider_override or get_settings().provider).strip().lower()
    if not provider:
        raise HTTPException(status_code=400, detail="PROVIDER is not set")
    return provider


def _parse_markdown_sections(markdown_text: str) -> tuple[str, str, str]:
    url = ""
    title = ""
    desc_lines = []
    current = None

    for line in markdown_text.splitlines():
        stripped = line.strip()
        lowered = stripped.lower()
        if lowered.startswith("url:") or lowered.startswith("url："):
            separator = "：" if "：" in stripped else ":"
            url = stripped.split(separator, 1)[-1].strip()
            current = None
            continue
        if lowered.startswith("title:") or lowered.startswith("title："):
            separator = "：" if "：" in stripped else ":"
            title = stripped.split(separator, 1)[-1].strip()
            current = None
            continue
        if lowered.startswith("desc:") or lowered.startswith("desc："):
            current = "desc"
            separator = "：" if "：" in stripped else ":"
            remainder = stripped.split(separator, 1)[-1].strip()
            if remainder:
                desc_lines.append(remainder)
            continue
        if current == "desc":
            desc_lines.append(line)

    desc = "\n".join(desc_lines).strip()
    if not url and not title and not desc:
        return "", "", markdown_text.strip()
    if not desc:
        desc = markdown_text.strip()
    return url, title, desc


async def _analyze_image(
    prompt: str,
    image_bytes: bytes,
    content_type: str,
    provider_override: Optional[str],
) -> LLMResult:
    provider_name = _get_provider_name(provider_override)
    try:
        provider = registry.get(provider_name)
        data = await provider.analyze_image(prompt, image_bytes, content_type)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    
    return LLMResult(markdown=data)


async def _store_in_memos(
    prompt: str,
    llm: LLMResult,
    image_bytes: bytes,
    content_type: str,
    filename: str,
    imgbool: bool,
) -> Optional[MemosResult]:
    
    settings = get_settings()
    client = MemosClient(settings.memos_base_url, settings.memos_token)
    if not client.enabled:
        raise HTTPException(status_code=400, detail="MEMOS_TOKEN is not set")

    # create memo
    memo_name = await client.create_memo(llm.markdown)
    if not memo_name:
        raise HTTPException(status_code=502, detail="Failed to create memo")
    
    # upload img if user enables to do it.
    if imgbool:
        attachment = await client.upload_attachment(image_bytes, filename, content_type)
        await client.set_memo_attachments(memo_name, attachment.name, filename, content_type)
    
    
    return MemosResult(memo_name=memo_name, attachment=attachment)


@app.post("/v1/image/data", response_model=ImageResponse)
async def parse_image_data(
    image: UploadFile = File(...),
    prompt: str = Form(...),
    imgbool: bool = Form(False),
    provider: Optional[str] = Form(None),
):
    image_bytes = await image.read()
    if not image_bytes:
        raise HTTPException(status_code=400, detail="Empty image file")
    
    content_type = image.content_type or "application/octet-stream"
    # call llm
    llm = await _analyze_image(prompt, image_bytes, content_type, provider)
    # store to memos
    memos = await _store_in_memos(
        prompt,
        llm,
        image_bytes,
        content_type,
        image.filename,
        imgbool,
    )
    return ImageResponse(llm=llm, memos=memos)


@app.post("/v1/image/json", response_model=ImageResponse)
async def parse_image_json(payload: ImageJsonRequest):
    try:
        image_bytes = base64.b64decode(payload.image_base64)
    except (ValueError, TypeError) as exc:
        raise HTTPException(status_code=400, detail="Invalid base64 image") from exc
    if not image_bytes:
        raise HTTPException(status_code=400, detail="Empty image payload")
    content_type = payload.content_type or "application/octet-stream"
    filename = payload.filename or "image.bin"
    llm = await _analyze_image(payload.prompt, image_bytes, content_type, payload.provider)
    memos = await _store_in_memos(
        payload.prompt,
        llm,
        image_bytes,
        content_type,
        filename,
        payload.upload_to_memos,
    )
    return ImageResponse(llm=llm, memos=memos)
