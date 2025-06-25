from langchain.agents import AgentExecutor
from langchain_core.messages import AIMessage, HumanMessage
from app.agents.employee_management.agent import create_agent_executor

class EmployeeService:
    def __init__(self):
        self.agent_executor: AgentExecutor = create_agent_executor()

    def process_employee_message(self, user_input: str, chat_history: list) -> dict:
        """Processes a user's employee management message by invoking the agent."""
        langchain_chat_history = []
        for message in chat_history:
            if message.get("role") == "human":
                langchain_chat_history.append(HumanMessage(content=message["content"]))
            elif message.get("role") == "ai":
                langchain_chat_history.append(AIMessage(content=message["content"]))

        response = self.agent_executor.invoke(
            {"input": user_input, "chat_history": langchain_chat_history}
        )
        return response

# Create a single, reusable instance of the service
employee_service = EmployeeService()

def get_employee_service() -> EmployeeService:
    """Dependency injector for the EmployeeService."""
    return employee_service
