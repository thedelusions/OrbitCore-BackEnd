from pydantic import BaseModel

class UserSchema(BaseModel):
    username: str  # User's unique name
    email: str  # User's email address
    password: str  # Plain text password for user registration (will be hashed before saving)
    role: str  # User's tech role
    bio: str  # User biography
    github_profile: str  # GitHub profile link

    class Config:
        from_attributes = True  # Enables compatibility with ORM models

# Schema for returning user data (without exposing the password)
class UserResponseSchema(BaseModel):
    id: int
    username: str
    email: str
    role: str
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
    role: str = None
    bio: str = None
    github_profile: str = None

    class Config:
        from_attributes = True