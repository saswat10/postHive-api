from typing import Optional
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy import func

from app import ouath2
from .. import models, schemas, utils
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # hash the password
    hashed_pwd = utils.hash(user.password)
    user.password = hashed_pwd

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=schemas.User)
def get_user(id: int, db: Session = Depends(get_db)):
    user = (
        db.query(
            models.User,
            func.coalesce(func.count(models.Post.id), 0).label("posts"),
            func.coalesce(func.count(models.Comments.id), 0).label("comments")
        )
        .outerjoin(models.Post, models.Post.owner_id == models.User.id)
        .outerjoin(models.Comments, models.Comments.user_id == models.User.id)
        .group_by(models.User.id)
        .filter(models.User.id == id)
        .first()    
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} does not exist",
        )

    response = user[0].__dict__

    return response
