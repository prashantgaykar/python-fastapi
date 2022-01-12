from typing import List
from fastapi import FastAPI, HTTPException, status, Response, APIRouter
from sqlalchemy.orm.session import Session
from fastapi.params import Depends

from app import oauth2
from .. import schemas, models
from ..database import get_db


router = APIRouter(prefix="/posts", tags=['Posts'])


@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.Post, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    new_post = models.Post(**post.dict(), user_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id : {id} not found"
        )
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id : {id} not found")
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"You are not allowed to delete the post with id : {id}")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}")
def update_post(id: int, post: schemas.Post, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    old_post_query = db.query(models.Post).filter(models.Post.id == id)
    old_post = old_post_query.first()
    if not old_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id : {id} not found")

    if old_post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"You are not allowed to delete the post with id : {id}")
                            
    old_post_query.update(post.dict())
    db.commit()
    return {"data": "updated successfully."}
