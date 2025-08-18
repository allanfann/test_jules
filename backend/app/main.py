from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.firebase_setup import lifespan

app = FastAPI(
    title="Core Processing Service",
    description="A service for processing unstructured text data and traversing decision trees.",
    version="0.2.0",
    lifespan=lifespan,
)


@app.get("/health", summary="Health Check", tags=["Monitoring"])
def health_check():
    """Health check endpoint to verify that the service is running."""
    return {"status": "ok"}


app.include_router(api_router, prefix="/api/v1")






