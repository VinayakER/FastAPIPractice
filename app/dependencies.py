from typing import Annotated

from fastapi import Depends, HTTPException, status
from .database import SessionLocal
from fastapi.security import OAuth2PasswordBearer
from .schemas import User, TokenData
from .utils import SECRET_KEY, ALGORITHM
from jose import jwt, JWTError
from .crud import get_user_by_email
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


#Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# # Fake function to decode token
# def fake_decode_token(token):
#     return User(
#         id=1,email="test@example.com", is_active=True
#     )

# Get current user dependency

def get_current_user(token:Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code= status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate":"Bearer"},
    )
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username : str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(db, email=token_data.username)
    if not user:
        raise credentials_exception

    return user

