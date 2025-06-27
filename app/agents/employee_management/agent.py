from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent, AgentExecutor

from app.agents.employee_management.tools import (
    list_active_employees,
    list_terminated_employees,
    get_employee_details,
    get_employee_by_name,
    get_employees_by_company,
    get_employees_by_status,
    get_employees_by_cost_center,
    get_employee_salary_info,
    get_employees_by_date_range,
    greet_employee_manager,
    get_distinct_values_summary,
    error_response,
)
from app.core.config import settings

def create_agent_executor():
    """Creates the agent for employee management."""
    tools = [
        list_active_employees,
        list_terminated_employees,
        get_employee_details,
        get_employee_by_name,
        get_employees_by_company,
        get_employees_by_status,
        get_employees_by_cost_center,
        get_employee_salary_info,
        get_employees_by_date_range,
        greet_employee_manager,
        get_distinct_values_summary,
        error_response,
    ]

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful employee database assistant with READ-ONLY access. Follow these rules precisely:\n\n"
                "RULES:\n"
                "1. You can ONLY search for, filter, and retrieve employee information.\n"
                "2. You CANNOT add, update, modify, or delete any employee data.\n"
                "3. If a user asks to add, update, modify, or delete employee data, "
                "use the `Error_response` tool to explain that these operations are not supported.\n"
                "4. If you need more information to search (like an employee name, ID, company, etc.), "
                "ask the user for it first.\n"
                "5. **CRITICAL RULE:** After a tool runs and returns information, "
                "your final answer MUST be that information. Do not add extra "
                "conversation or ask what to do next. Just provide the data.\n"
                "6. When dealing with dates, use YYYY-MM-DD format.\n"
                "7. For salary information, format numbers with commas and currency symbols when appropriate.\n"
                "8. Always distinguish between active and terminated employees when relevant.\n"
                "9. When searching by date ranges, ask for clarification on which type of date "
                "(admission, termination, or birth) if not specified.\n"
                "10. Use the `get_employee_by_name` tool for name-based searches (supports partial matches).",
            ),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    llm = ChatGroq(
        model_name="llama3-70b-8192",
        temperature=0,
        groq_api_key=settings.GROQ_API_KEY,
    )

    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    return agent_executor
