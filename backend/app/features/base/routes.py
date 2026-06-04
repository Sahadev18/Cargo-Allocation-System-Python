from fastapi import APIRouter

from app.core.config import settings

router = APIRouter()


@router.get("/", tags=["base"])
async def api_base() -> dict[str, str]:
    return {
        "name": settings.app_name,
        "version": "v1",
        "status": "ready",
    }
