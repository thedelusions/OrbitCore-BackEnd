from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from models.project import ProjectStatus


class ProjectSchema(BaseModel):
    title: str
    description: str
    ownerId: int
    status: Optional[ProjectStatus] = ProjectStatus.OPEN
    tags: Optional[str] = None
    repo_link: Optional[str] = None

    class Config:
        from_attributes = True


class ProjectResponseSchema(BaseModel):
    id: int
    title: str
    description: str
    ownerId: int
    status: ProjectStatus
    tags: Optional[str] = None
    repo_link: Optional[str] = None
    upvotes: int
    downvotes: int
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True


class ProjectUpdateSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[ProjectStatus] = None
    tags: Optional[str] = None
    repo_link: Optional[str] = None

    class Config:
        from_attributes = True
