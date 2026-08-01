from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user, require_roles
from app.schemas.user import CurrentUser

api_router = APIRouter()


@api_router.get("/status", tags=["status"])
async def api_status():
    return {
        "status": "ok",
        "api_version": "v1",
    }


@api_router.get("/me", tags=["users"])
async def get_me(current_user: CurrentUser = Depends(get_current_user)):
    return current_user


@api_router.get("/admin/status", tags=["admin"])
async def admin_status(
    current_user: CurrentUser = Depends(require_roles("admin")),
):
    return {
        "status": "ok",
        "admin": current_user.id,
    }