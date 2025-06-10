from pydantic import BaseModel
from typing import List, Dict, Any

class ChatRequest(BaseModel):
    """Request model for the chat endpoint."""
    user_input: str
    chat_history: List[Dict[str, Any]] = []

class ChatResponse(BaseModel):
    """Response model for the chat endpoint."""
    agent_output: str
    chat_history: List[Dict[str, Any]]