from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from models.user import UserModel
from database import get_db
import jwt
from jwt import DecodeError, ExpiredSignatureError # We import specific exceptions to handle them explicitly
from config.environment import secret

# We're using the HTTP Bearer scheme for the Authorization header
http_bearer = HTTPBearer()

# This function takes the database session and the JWT token from the request header
def get_current_user(db: Session = Depends(get_db), token: str = Depends(http_bearer)):

    try:
        # Decode the token using the secret key
        payload = jwt.decode(token.credentials, secret, algorithms=["HS256"])

        # Query the database to find the user with the ID from the token's payload
        user = db.query(UserModel).filter(UserModel.id == int(payload.get("sub"))).first()

        # If no user is found, raise an HTTP 401 Unauthorized error
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                 detail="Invalid username or password")

    # Handle decoding errors (invalid token)
    except DecodeError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                             detail=f'Could not decode token: {str(e)}')

    # Handle expired token errors
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                             detail='Token has expired')

    # Return the user if the token is valid
    return user
