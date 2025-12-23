from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from serializers.user import UserResponseSchema

class TeamSchema(BaseModel):
    project_id: int
    user_id: int
    role: str
    repo_link: Optional[str] = None

    class Config:
        from_attributes = True

class TeamResponseSchema(BaseModel):
    id: int
    project_id: int
    user_id: int
    role: str
    repo_link: Optional[str] = None
    joined_at: Optional[datetime] = None
    user: UserResponseSchema

    class Config:
        from_attributes = True
