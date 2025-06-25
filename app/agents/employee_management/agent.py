from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent, AgentExecutor

from app.agents.employee_management.tools import (
    list_all_employees,
    list_active_employees,
    list_terminated_employees,
    get_employee_details,
    get_employee_by_name,
    get_employees_by_company,
    get_employees_by_status,
    get_employees_by_cost_center,
    get_employee_salary_info,
    get_employees_by_date_range,
    add_new_employee,
    update_employee_details,
    delete_employee,
    greet_employee_manager,
)
from app.core.config import settings

def create_agent_executor():
    """Creates the agent for employee management."""
    tools = [
        # list_all_employees,
        list_active_employees,
        list_terminated_employees,
        get_employee_details,
        get_employee_by_name,
        get_employees_by_company,
        get_employees_by_status,
        get_employees_by_cost_center,
        get_employee_salary_info,
        get_employees_by_date_range,
        add_new_employee,
        update_employee_details,
        delete_employee,
        greet_employee_manager,
    ]

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful employee database assistant. Follow these rules precisely:\n\n"
                "RULES:\n"
                "1. First, understand the user's goal (e.g., add, update, list, search, etc.).\n"
                "2. If the user's goal is to 'update', 'modify', or 'change' employee data, "
                "you MUST use the `update_employee_details` tool and are FORBIDDEN "
                "from using `add_new_employee`.\n"
                "3. If you need more information to use a tool (like an employee ID, company name, etc.), "
                "you MUST ask the user for it first.\n"
                "4. **CRITICAL RULE:** After a tool runs, if it returns information "
                "(like a list of employees or employee details), your final answer "
                "MUST be that information and nothing else. Do not add extra "
                "conversation or ask what to do next. Just provide the data.\n"
                "5. When dealing with dates, use YYYY-MM-DD format.\n"
                "6. For salary information, format numbers with commas and currency symbols when appropriate.\n"
                "7. Always distinguish between active and terminated employees when relevant.\n"
                "8. When searching by date ranges, ask for clarification on which type of date "
                "(admission, termination, or birth) if not specified.",
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
