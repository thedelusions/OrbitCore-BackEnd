from pydantic import BaseModel, field_validator
from typing import Optional, List, Dict
from datetime import datetime
from models.project import ProjectStatus


class MemberRole(BaseModel):
    role: str
    count: int

class ProjectSchema(BaseModel):
    title: str
    description: str
    ownerId: int
    status: Optional[ProjectStatus] = ProjectStatus.OPEN
    tags: List[str]
    repo_link: Optional[str] = None
    required_members: Optional[int] = None
    members_roles: List[MemberRole] = []
    
    @field_validator('tags')
    @classmethod
    def validate_tags(cls, v):
        if len(v) > 5:
            raise ValueError('Maximum 5 tags allowed')
        if len(v) == 0:
            raise ValueError('At least 1 tag required')
        return v

    class Config:
        from_attributes = True


class ProjectResponseSchema(BaseModel):
    id: int
    title: str
    description: str
    ownerId: int
    status: ProjectStatus
    tags: List[str]
    repo_link: Optional[str] = None
    required_members: Optional[int] = None
    members_roles: List[MemberRole]
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
    tags: Optional[List[str]] = None
    repo_link: Optional[str] = None
    required_members: Optional[int] = None
    members_roles: Optional[List[MemberRole]] = None
    
    @field_validator('tags')
    @classmethod
    def validate_tags(cls, v):
        if v is not None:
            if len(v) > 5:
                raise ValueError('Maximum 5 tags allowed')
            if len(v) == 0:
                raise ValueError('At least 1 tag required')
        return v

    class Config:
        from_attributes = True
