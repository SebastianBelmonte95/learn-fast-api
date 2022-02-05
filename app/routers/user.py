from .. import utils
from .. import models
from ..database import get_db
from sqlalchemy.orm import Session
from .. import schemas
from fastapi import APIRouter, FastAPI, status, HTTPException, Depends, APIRouter

router = APIRouter()

@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Hashing the password ~ user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    # Creating new user
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/users/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} does not exist",
        )
    return user