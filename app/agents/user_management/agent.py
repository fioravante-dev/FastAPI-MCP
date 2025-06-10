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
                "You are a helpful database assistant. Follow these rules precisely:\n\n"
                "RULES:\n"
                "1. First, understand the user's goal (e.g., add, update, list, etc.).\n"
                "2. If the user's goal is to 'update', 'modify', or 'change' data, "
                "you MUST use the `update_user_details` tool and are FORBIDDEN "
                "from using `add_new_user`.\n"
                "3. If you need more information to use a tool (like a name or email), "
                "you MUST ask the user for it first.\n"
                "4. **CRITICAL RULE:** After a tool runs, if it returns information "
                "(like a list of users or a user's details), your final answer "
                "MUST be that information and nothing else. Do not add extra "
                "conversation or ask what to do next. Just provide the data.",
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