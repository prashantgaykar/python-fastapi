
from typing import List
from fastapi import FastAPI, HTTPException, status, APIRouter
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import IntegrityError
from fastapi.params import Depends
from .. import schemas,models,util
from ..database import  get_db

router = APIRouter(prefix="/users",tags=['Users'])

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    user.password = util.hash(user.password)
    new_user = models.User(**user.dict())
    try:
        db.add(new_user)
        db.commit()
        return {"msg": "User created successfully."}
    except IntegrityError:
         raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"email id : {user.email} is already exist."
        )


@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id : {id} not found"
        )
    return user
