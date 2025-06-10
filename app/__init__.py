from fastapi import FastAPI
from app.api.routers import chat_router, status_router

app = FastAPI(
    title="Multi-Agent API (Working Version)",
    description="An API to test agent functionality.",
    version="2.0.0",
)

app.include_router(status_router.router, prefix="/api/v1", tags=["System"])
app.include_router(chat_router.router, prefix="/api/v1", tags=["Chat"])

print("FastAPI application configured and ready.")