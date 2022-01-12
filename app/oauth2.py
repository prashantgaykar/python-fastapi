
from datetime import datetime, timedelta
from fastapi.params import Depends
from jose import jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status
from jose.exceptions import JWTError
from sqlalchemy.orm.session import Session
from app import models, schemas
from app.database import get_db
from .config import settings


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRES_MINUTES = settings.access_token_expires_minutes

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token, credential_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        id = payload.get("user_id")
        if id is None:
            raise credential_exception
        token_data = schemas.TokenData(id=id)
        return token_data
    except JWTError:
        raise credential_exception


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = verify_access_token(token,credentials_exception)

    user = db.query(models.User).filter(models.User.email == token_data.id).first()

    return user
