from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.user import UserModel
from serializers.user import UserSchema, UserLogin, UserToken, UserResponseSchema, UserUpdateSchema
from database import get_db
from dependencies.get_current_user import get_current_user
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

@router.get("/users/{user_id}", response_model=UserResponseSchema)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/profile", response_model=UserResponseSchema)
def get_profile(current_user: UserModel = Depends(get_current_user)):
    return current_user

@router.put("/profile", response_model=UserResponseSchema)
def update_profile(update_data: UserUpdateSchema, current_user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    if update_data.role is not None:
        current_user.role = update_data.role
    if update_data.bio is not None:
        current_user.bio = update_data.bio
    if update_data.github_profile is not None:
        current_user.github_profile = update_data.github_profile
    db.commit()
    db.refresh(current_user)
    return current_user