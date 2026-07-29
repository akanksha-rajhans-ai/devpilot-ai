from fastapi import APIRouter

api_router = APIRouter()


@api_router.get("/status", tags=["status"])
async def api_status():
    return {
        "status": "ok",
        "api_version": "v1",
    }