from pydantic import BaseModel
from datetime import datetime
from serializers.user import UserResponseSchema
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
    user: UserResponseSchema
    class Config:
        from_attributes = True