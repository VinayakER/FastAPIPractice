from passlib.context import CryptContext
from . import models
from datetime import timedelta, datetime
from sqlalchemy.orm import Session

from jose import JWTError, jwt

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

SECRET_KEY = "d817feb970dfd8ecc60bcb413d68531acabacedcf012f1de9f2bb997a9bd2fbc"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30



def verify_password(plain_password, hashed_password):
    print(plain_password,hashed_password)
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(db:Session, username: str, password:str):
    user = db.query(models.User).filter(models.User.email==username).first()
    if not user:
        return False

    if not verify_password(password, user.hashed_password):
        return False

    return user

def create_access_token(data : dict, expires_delta : timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm =ALGORITHM)
    return encoded_jwt