from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, ouath2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func, select

router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user=Depends(ouath2.get_current_user),
):
    new_post = models.Post(**post.dict(), owner_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/", response_model=List[schemas.PostWithVotes])
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0):

    
    posts = (
        db.query(
            models.Post,
            func.coalesce(func.count(models.Vote.post_id), 0).label("votes"),
            func.coalesce(func.count(models.Comments.id), 0).label("comments")
        )
        .outerjoin(models.Vote, models.Vote.post_id == models.Post.id)
        .outerjoin(models.Comments, models.Comments.post_id == models.Post.id)
        .group_by(models.Post.id)  
        .order_by(models.Post.id.asc())
        .limit(limit)
        .offset(skip)
        .all()
    )

    return [
        {
            **post[0].__dict__,
            "votes": post[1],
            "comments": post[2],
            "owner": db.query(models.User)
            .filter(models.User.id == post[0].owner_id)
            .first(),
        }
        for post in posts
    ]


@router.get("/{id}", response_model=schemas.PostWithVotes)
def get_post(id: int, db: Session = Depends(get_db)):
    result = (
        db.query(
            models.Post,
            func.coalesce(func.count(models.Vote.post_id), 0).label("votes"),
            func.coalesce(func.count(models.Comments.id), 0).label("comments")
        )
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .join(models.Comments, models.Comments.post_id == models.Post.id, isouter=True)
        .group_by(models.Post)
        .filter(models.Post.id == id)
        .first()
    )

    if not result:
        raise HTTPException(status_code=404, detail="Post not found")

    post = result[0].__dict__
    post["votes"] = result[1]
    post["comments"] = result[2]
    post["owner"] = (
        db.query(models.User).filter(models.User.id == result[0].owner_id).first()
    )

    return post


@router.put("/{id}", response_model=schemas.Post)
def update_post(
    id: int,
    updated_post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user=Depends(ouath2.get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to perform action")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(ouath2.get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to perform action")

    post_query.delete(synchronize_session=False)
    db.commit()
    return


@router.get(
    "/{post_id}/comments/", response_model=List[schemas.Comment], tags=["Comments"]
)
def get_comments(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    comments = (
        db.query(models.Comments).filter(models.Comments.post_id == post_id).all()
    )
    return comments


@router.post("/{post_id}/comments/", response_model=schemas.Comment, tags=["Comments"])
def create_comment(
    post_id: int,
    comment: schemas.CommentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(ouath2.get_current_user),
):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    new_comment = models.Comments(
        **comment.dict(), post_id=post_id, user_id=current_user.id
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment
