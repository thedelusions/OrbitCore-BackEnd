
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from serializers.user import UserResponseSchema
from serializers.project import ProjectResponseSchema

class RequestCreateSchema(BaseModel):
    role: str
    message: Optional[str] = None

    class Config:
        from_attributes = True


class RequestUpdateSchema(BaseModel):
    status: str  # "pending", "accepted", or "rejected"

    class Config:
        from_attributes = True


class RequestResponseSchema(BaseModel):
    id: int
    project_id: int
    user_id: int
    role: str
    status: str
    message: Optional[str] = None
    createdAt: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class RequestWithDetailsSchema(BaseModel):
    id: int
    project_id: int
    user_id: int
    role: str
    status: str
    message: Optional[str] = None
    createdAt: datetime
    updated_at: datetime
    user: UserResponseSchema
    project: ProjectResponseSchema

    class Config:
        from_attributes = True