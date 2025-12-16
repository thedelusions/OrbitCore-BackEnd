from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class RequestCreateSchema(BaseModel):
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
    status: str
    message: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class RequestWithDetailsSchema(BaseModel):
    id: int
    project_id: int
    user_id: int
    status: str
    message: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    user: dict  
    project: dict 

    class Config:
        from_attributes = True
