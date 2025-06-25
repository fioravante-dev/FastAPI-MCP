from fastapi import APIRouter, Depends
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.employee_service import EmployeeService, get_employee_service

router = APIRouter()

@router.post("/employee/chat", response_model=ChatResponse)
async def chat_with_employee_agent(
    request: ChatRequest,
    employee_service: EmployeeService = Depends(get_employee_service),
):
    """Main endpoint to chat with the employee management AI agent."""
    response = employee_service.process_employee_message(
        user_input=request.user_input, chat_history=request.chat_history
    )

    agent_output = response["output"]
    updated_history = request.chat_history + [
        {"role": "human", "content": request.user_input},
        {"role": "ai", "content": agent_output},
    ]

    return ChatResponse(agent_output=agent_output, chat_history=updated_history)

@router.get("/employee/help")
async def get_employee_help():
    """Get help information about employee management capabilities."""
    return {
        "message": "Employee Management Agent Help",
        "capabilities": [
            "📊 List all employees, active employees, or terminated employees",
            "🔍 Search employees by ID, company, status, or cost center", 
            "📅 Filter employees by date ranges (admission, termination, birth dates)",
            "💰 Get detailed salary information for specific employees",
            "👥 Add new employees with comprehensive details",
            "✏️ Update existing employee information",
            "🗑️ Delete employee records",
            "🏢 Get company-specific employee lists",
            "📋 Filter by employment status or cost centers"
        ],
        "examples": [
            "List all active employees",
            "Show me employee details for ID EMP001",
            "Find all employees in Marketing department",
            "Get salary information for John Doe",
            "Add a new employee named Jane Smith",
            "Update employee EMP002's salary to 75000",
            "Show employees hired between 2023-01-01 and 2023-12-31"
        ]
    }