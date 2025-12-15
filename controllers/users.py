from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.user import UserModel
from serializers.user import UserSchema, UserLogin, UserToken, UserResponseSchema
from database import get_db

router = APIRouter()

@router.post("/register", response_model=UserResponseSchema)
def create_user(user: UserSchema, db: Session = Depends(get_db)):
    # Check if the username or email already exists
    existing_user = db.query(UserModel).filter(
        (UserModel.username == user.username) | (UserModel.email == user.email)
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already exists")

    new_user = UserModel(
        username=user.username,
        email=user.email,
        role=user.role,
        bio=user.bio,
        github_profile=user.github_profile
    )
    # Use the set_password method to hash the password
    new_user.set_password(user.password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/login", response_model=UserToken)
def login(user: UserLogin, db: Session = Depends(get_db)):

    # Find the user by username
    db_user = db.query(UserModel).filter(UserModel.username == user.username).first()

    # Check if the user exists and if the password is correct
    if not db_user or not db_user.verify_password(user.password):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    # Generate JWT token
    token = db_user.generate_token()

    # Return token and a success message
    return {"token": token, "message": "Login successful"}