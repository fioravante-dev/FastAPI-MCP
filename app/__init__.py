# app/__init__.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.routers import chat_router, status_router
from app.persistence.database import init_db_pool, create_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code to run on application startup
    print("Application startup...")
    # 1. Initialize the database connection pool
    init_db_pool()
    # 2. Now that the pool is ready, create the tables
    create_tables()
    print("Database setup complete.")
    yield
    # Code to run on application shutdown
    print("Application shutting down.")

# Create the main FastAPI application instance with the lifespan manager
app = FastAPI(
    title="Multi-Agent API",
    description="A professional, layered API for interacting with AI agents.",
    version="1.0.0",
    lifespan=lifespan,
)

# Include the different API routers
app.include_router(status_router.router, prefix="/api/v1", tags=["System"])
app.include_router(chat_router.router, prefix="/api/v1", tags=["Chat"])