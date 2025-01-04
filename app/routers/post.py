from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, ouath2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import case, func, select

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
def get_posts(db: Session = Depends(get_db), limit: int = 100, skip: int = 0, current_user= Depends(ouath2.get_current_user)):

    
    posts = (
        db.query(models.Post)
        .order_by(models.Post.created_at.desc())
        .limit(limit)
        .offset(skip)
        .all()
    )

    # Fetch votes for the current user
    user_votes = {
        vote.post_id
        for vote in db.query(models.Vote)
        .filter(models.Vote.user_id == current_user.id)
        .all()
    }

    # Count votes for each post
    votes_count = {
        post_id: count
        for post_id, count in db.query(models.Vote.post_id, func.count(models.Vote.post_id))
        .group_by(models.Vote.post_id)
        .all()
    }

    # Count comments for each post
    comments_count = {
        post_id: count
        for post_id, count in db.query(models.Comments.post_id, func.count(models.Comments.post_id))
        .group_by(models.Comments.post_id)
        .all()
    }

    return [
        {
            **post.__dict__,
            "votes": votes_count.get(post.id, 0),
            "comments": comments_count.get(post.id, 0),
            "has_voted": post.id in user_votes,
            "owner": db.query(models.User)
            .filter(models.User.id == post.owner_id)
            .first(),
        }
        for post in posts
    ]


@router.get("/{id}", response_model=schemas.PostWithVotes)
def get_post(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(ouath2.get_current_user),
):
    # Fetch the post
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Fetch votes count
    votes_count = (
        db.query(func.count(models.Vote.post_id))
        .filter(models.Vote.post_id == id)
        .scalar()
    )

    # Fetch comments count
    comments_count = (
        db.query(func.count(models.Comments.id))
        .filter(models.Comments.post_id == id)
        .scalar()
    )

    # Check if the user has voted
    has_voted = (
        db.query(models.Vote)
        .filter(models.Vote.post_id == id, models.Vote.user_id == current_user.id)
        .first()
        is not None
    )

    # Fetch post owner
    owner = db.query(models.User).filter(models.User.id == post.owner_id).first()

    return {
        **post.__dict__,
        "votes": votes_count,
        "comments": comments_count,
        "has_voted": has_voted,
        "owner": owner,
    }



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
