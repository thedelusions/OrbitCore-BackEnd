from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ProjectSchema(BaseModel):
    title: str
    description: str
    ownerId: int
    status: Optional[str] = "open"
    tags: Optional[str] = None

    class Config:
        from_attributes = True


class ProjectResponseSchema(BaseModel):
    id: int
    title: str
    description: str
    ownerId: int
    status: str
    tags: Optional[str] = None
    upvotes: int
    downvotes: int
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True


class ProjectUpdateSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    tags: Optional[str] = None

    class Config:
        from_attributes = True
