from pydantic import BaseModel, Field, field_validator
from typing import List

class UserSchema(BaseModel):
    username: str  # User's unique name
    email: str  # User's email address
    password: str = Field(min_length=8) # Plain text password for user registration (will be hashed before saving)
    roles: List[str]  # User's tech roles (max 3)
    bio: str  # User biography
    github_profile: str  # GitHub profile link
    
    @field_validator('roles')
    @classmethod
    def validate_roles(cls, v):
        if len(v) > 3:
            raise ValueError('Maximum 3 roles allowed')
        if len(v) == 0:
            raise ValueError('At least 1 role required')
        return v

    class Config:
        from_attributes = True  # Enables compatibility with ORM models

# Schema for returning user data (without exposing the password)
class UserResponseSchema(BaseModel):
    id: int
    username: str
    email: str
    roles: List[str]
    bio: str
    github_profile: str

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username: str  # Username provided by the user during login
    password: str  # Plain text password provided by the user during login

# New schema for the response (containing the JWT token and a success message)
class UserToken(BaseModel):
    token: str  # JWT token generated upon successful login
    message: str  # Success message

    class Config:
        from_attributes = True

class UserUpdateSchema(BaseModel):
    roles: List[str] = None
    bio: str = None
    github_profile: str = None
    
    @field_validator('roles')
    @classmethod
    def validate_roles(cls, v):
        if v is not None:
            if len(v) > 3:
                raise ValueError('Maximum 3 roles allowed')
            if len(v) == 0:
                raise ValueError('At least 1 role required')
        return v

    class Config:
        from_attributes = True