from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent, AgentExecutor

from app.agents.user_management.tools import (
    list_all_users,
    get_user_details,
    add_new_user,
    update_user_details,
    delete_user,
    greet_user,
)
from app.core.config import settings

def create_agent_executor():
    """Creates the agent for user management."""
    tools = [
        list_all_users,
        get_user_details,
        add_new_user,
        update_user_details,
        delete_user,
        greet_user,
    ]

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a database assistant. Your most important task is to "
                "distinguish between creating a NEW user and updating an "
                "EXISTING one.\n\n"
                "RULES:\n"
                "1. If the user's query contains words like 'update', 'modify', "
                "'change', or 'edit', you MUST use the `update_user_details` tool.\n"
                "2. Under these circumstances, you are FORBIDDEN from using the "
                "`add_new_user` tool.\n"
                "3. If you need more information, you MUST ask the user for it.\n"
                "4. Do not make up answers. If a tool fails, report the error "
                "and stop.",
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