from fastapi import APIRouter

from app.api.v1.endpoints import decision, legacy

api_router = APIRouter()
api_router.include_router(decision.router, prefix="/decision", tags=["Decision Trees"])
api_router.include_router(legacy.router, prefix="/legacy", tags=["Legacy Processing"])
