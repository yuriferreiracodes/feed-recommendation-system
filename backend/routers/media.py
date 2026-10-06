from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from backend.dependencies import StorageClient
from backend.services import media_service

router = APIRouter(tags=["media"])


@router.get(
    "/media/{key:path}",
    response_class=StreamingResponse,
    responses={
        200: {"content": {"image/*": {}}, "description": "The stored image bytes"},
        404: {"description": "No such media object"},
    },
)
def get_media(key: str, storage: StorageClient):
    """Stream an uploaded image out of object storage.

    Serving through the API keeps the bucket private and the URL permanent — no
    public bucket policy, no presigned URLs expiring inside a cached feed page.
    """
    stream, content_type, length, etag = media_service.open_media(storage, key)
    headers = {
        "Content-Length": str(length),
        # Keys are random per upload and never reused, so the bytes behind a key
        # can't change: safe to cache hard.
        "Cache-Control": "public, max-age=31536000, immutable",
    }
    if etag:
        headers["ETag"] = etag
    return StreamingResponse(stream, media_type=content_type, headers=headers)
