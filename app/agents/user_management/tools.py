from langchain_core.tools import tool
from app.persistence import user_repository
from app.schemas.user import (
    GetUserDetailsInput, AddUserInput, UpdateUserInput, DeleteUserInput
)

@tool
def list_all_users() -> str:
    """Lists all users currently in the database."""
    users = user_repository.list_all()
    if not users:
        return "There are no users in the database."
    return "\n".join([f"- {name} ({email})" for name, email in users])

@tool("get_user_details", args_schema=GetUserDetailsInput)
def get_user_details(name: str) -> str:
    """Finds a specific user by their name."""
    user = user_repository.get_by_name(name=name)
    if not user:
        return f"No user found with the name '{name}'."
    return f"User Details: Name={user['name']}, Email={user['email']}"

@tool("add_new_user", args_schema=AddUserInput)
def add_new_user(name: str, email: str) -> str:
    """Adds a new user to the database."""
    try:
        user_repository.add(name=name, email=email)
        return f"User '{name}' was successfully added."
    except Exception:
        return f"Error: A user with the email '{email}' might already exist."

@tool("update_user_details", args_schema=UpdateUserInput)
def update_user_details(name: str, new_name: str = None, new_email: str = None) -> str:
    """Modifies the details of an existing user."""
    if not new_name and not new_email:
        return "Error: You must provide a new name or a new email to update."
    try:
        rows_affected = user_repository.update(
            name=name, new_name=new_name, new_email=new_email
        )
        if rows_affected == 0:
            return f"Error: No user found with the name '{name}' to update."
        return f"Successfully updated user '{name}'."
    except Exception:
        return f"Error: The new email '{new_email}' might already be in use."

@tool("delete_user", args_schema=DeleteUserInput)
def delete_user(name: str) -> str:
    """Permanently deletes an existing user."""
    rows_affected = user_repository.delete(name=name)
    if rows_affected == 0:
        return f"Error: No user found with the name '{name}' to delete."
    return f"User '{name}' has been successfully deleted."

@tool(return_direct=True)
def greet_user() -> str:
    """Provides a greeting and explains the agent's capabilities."""
    return "Hello! I am a database management assistant. I can add, update, delete, find, and list users."