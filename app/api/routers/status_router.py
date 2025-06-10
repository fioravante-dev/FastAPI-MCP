from fastapi import APIRouter

router = APIRouter()

@router.get("/status")
def health_check():
    """A simple endpoint to confirm the API is running."""
    return {"status": "ok"}