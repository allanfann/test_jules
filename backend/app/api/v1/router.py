from fastapi import APIRouter

from app.api.v1.endpoints import decision
from app.api.v1.endpoints.analysis import personality
from app.api.v1.endpoints.processing import text

api_router = APIRouter()

api_router.include_router(decision.router, tags=["Decision Trees"])
api_router.include_router(personality.router, prefix="/analysis", tags=["Analysis"])
api_router.include_router(text.router, prefix="/processing", tags=["Processing"])
