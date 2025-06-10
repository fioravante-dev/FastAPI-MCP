from fastapi import APIRouter, Depends
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService, get_chat_service

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_with_agent(
    request: ChatRequest,
    chat_service: ChatService = Depends(get_chat_service),
):
    """Main endpoint to chat with the AI agent."""
    response = chat_service.process_chat_message(
        user_input=request.user_input, chat_history=request.chat_history
    )

    agent_output = response["output"]
    updated_history = request.chat_history + [
        {"role": "human", "content": request.user_input},
        {"role": "ai", "content": agent_output},
    ]

    return ChatResponse(agent_output=agent_output, chat_history=updated_history)