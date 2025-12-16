from pydantic import BaseModel
from datetime import datetime

class TeamSchema(BaseModel):
    project_id: int
    user_id: int
    role: str
    repo_link: str = None

    class Config:
        orm_mode = True

class TeamResponseSchema(BaseModel):
    id: int
    project_id: int
    user_id: int
    role: str
    repo_link: str = None
    joined_at: datetime

    class Config:
        orm_mode = True
