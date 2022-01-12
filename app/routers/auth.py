
from typing import List
from fastapi import FastAPI, HTTPException, status, APIRouter
from sqlalchemy.orm.session import Session
from fastapi.params import Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import schemas, models, util, oauth2
from ..database import get_db

router = APIRouter(prefix="/login", tags=['Authentication'])


@router.post("/", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    print("login()")
    saved_user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()
    if not saved_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials."
        )

    is_verified = util.verify(user_credentials.password, saved_user.password)
    if not is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials."
        )

    token = oauth2.create_access_token(data={"user_id": user_credentials.username})
    return {"access_token": token, "token_type": "bearer"}
