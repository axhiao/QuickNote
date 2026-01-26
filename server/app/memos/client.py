import base64
import httpx

from typing import Optional
from app.models.schemas import MemosAttachment


class MemosClient:
    def __init__(self, base_url: str, token: str, user_id: int) -> None:
        self._base_url = base_url.rstrip("/")
        self._token = token
        self._user_id = user_id 

    @property
    def enabled(self) -> bool:
        return bool(self._token)

    # 1. create a memo
    async def create_memo(self, content: str) -> Optional[str]:
        headers = {
            "Authorization": f"Bearer {self._token}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "state": "STATE_UNSPECIFIED",
            "content": content,
            "visibility": "VISIBILITY_UNSPECIFIED",
        }
        
        async with httpx.AsyncClient(base_url=self._base_url, timeout=30) as client:
            response = await client.post("/api/v1/memos", json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
        
        return data.get("name")
    
    # 2. upload an attachment
    async def upload_attachment(
        self,
        image_bytes: bytes,
        filename: str,
        content_type: str,
    ) -> MemosAttachment:
        payload = {
            "filename": filename,
            "type": content_type,
            "content": base64.b64encode(image_bytes).decode("ascii"),
        }
        headers = {
            "Authorization": f"Bearer {self._token}",
            "Content-Type": "application/json",
        }
        async with httpx.AsyncClient(base_url=self._base_url, timeout=30) as client:
            response = await client.post("/api/v1/attachments", json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
        return MemosAttachment(
            name=data.get("name", ""),
            filename=filename,
            content_type=content_type,
        )

    # 3. bind an attachement with a memo.
    async def set_memo_attachments(self, memo_name: str, attachment_name: str, filename: str, content_type: str) -> None:
        
        # print("--------- \t ", memo_name) memos/nK53rkiHvNg8CFawR9tPSH
        # print("--------- \t ", attachment_name) attachments/kAmXPU5dzGCBU2Bc8zKzFo
        
        payload = {
            "name": attachment_name.lstrip("attachments/"),
            "attachments": [
                {
                    "name" : attachment_name,
                    "filename": filename,
                    "type": content_type
                }
            ]
        }

        headers = {
            "Authorization": f"Bearer {self._token}",
            "Content-Type": "application/json",
        }
        memo_id = memo_name[len("memos/"):] if memo_name.startswith("memos/") else memo_name
        endpoint = f"/api/v1/memos/{memo_id}/attachments"
        async with httpx.AsyncClient(base_url=self._base_url, timeout=30) as client:
            response = await client.patch(endpoint, json=payload, headers=headers)
            response.raise_for_status()

    
    #
    async def user_tags(self, ) -> dict[str, int]:
        headers = {
            "Authorization": f"Bearer {self._token}",
            "Content-Type": "application/json",
        }
        async with httpx.AsyncClient(base_url=self._base_url, timeout=30) as client:
            response = await client.get(f"/api/v1/users/{self._user_id}:getStats", headers=headers)
            response.raise_for_status()
            data = response.json()
            return data["tagCount"]
        