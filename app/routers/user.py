from typing import Optional
from fastapi import status, HTTPException, Depends, APIRouter

from app import ouath2
from .. import models, schemas, utils
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # hash the password
    hashed_pwd = utils.hash(user.password)
    user.password = hashed_pwd

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    db.commit()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} does not exist",
        )

    return user

@router.get("/{id}/posts", response_model=schemas.UserPostsResponse)
def get_user_posts(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(ouath2.get_current_user)
):
    posts_query = (
        db.query(models.Post)
        .filter(models.Post.owner_id == id)
        .order_by(models.Post.created_at.desc())  # Optional: order by most recent
    )
    posts = [
        {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "created_at": post.created_at,
            "votes_count": db.query(models.Vote).filter(models.Vote.post_id == post.id).count(),
            "comments_count": db.query(models.Comments).filter(models.Comments.post_id == post.id).count(),
            "upvoted": (db.query(models.Vote).filter(models.Vote.post_id == post.id, models.Vote.user_id == current_user.id).first() is not None)
        }
        for post in posts_query
    ]

    # Construct response
    return {
        "user_id": id,
        "posts_count": len(posts),
        "posts": posts,
    }