from pydantic import BaseModel
from datetime import datetime

class CommentSchema(BaseModel):
    content: str

    class Config:
        from_attributes = True

class CommentResponseSchema(BaseModel):
    id: int
    team_id: int
    user_id: int
    content: str
    created_at: datetime

    class Config:
        from_attributes = True