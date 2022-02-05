from typing import List
from .. import models
from ..database import get_db
from sqlalchemy.orm import Session
from .. import schemas
from fastapi import (
    APIRouter,
    status,
    HTTPException,
    Depends,
    APIRouter,
    Response,
)

router = APIRouter()


@router.get("/posts", response_model=List[schemas.PostBase])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@router.post(
    "/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostBase
)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/posts/{id}", response_model=schemas.PostBase)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found",
        )
    return post


@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    if deleted_post.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found",
        )
    deleted_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/posts/{id}", response_model=schemas.PostBase)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found",
        )
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
