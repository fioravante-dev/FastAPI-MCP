from pydantic import BaseModel, Field
from typing import Optional

class GetUserDetailsInput(BaseModel):
    name: str = Field(description="The name of the user to search for.")

class AddUserInput(BaseModel):
    name: str = Field(description="The full name of the new user.")
    email: str = Field(description="The unique email address for the new user.")

class UpdateUserInput(BaseModel):
    name: str = Field(description="The name of the user to be updated.")
    new_name: Optional[str] = Field(
        default=None, description="The user's new name. (Optional)"
    )
    new_email: Optional[str] = Field(
        default=None, description="The user's new email address. (Optional)"
    )

class DeleteUserInput(BaseModel):
    name: str = Field(description="The name of the user to be deleted.")