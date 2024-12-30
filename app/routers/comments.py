from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, ouath2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func

router = APIRouter(prefix="/comments", tags=["Comments"])


# create a comment
@router.post(
    "/post_id/{post_id}",
    response_model=schemas.CommentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_comment(
    post_id: int,
    comment: schemas.CommentCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(ouath2.get_current_user),
):
    new_comment = models.Comments(user_id=current_user.id, **comment.model_dump())
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post_first = post_query.first()

    if not post_first:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id:{post_id} was not found",
        )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


# update a comment
@router.put("/{comment_id}", response_model=schemas.CommentResponse)
def update_comment(
    comment_id: int,
    comment: schemas.CommentUpdate,
    db: Session = Depends(get_db),
    current_user: int = Depends(ouath2.get_current_user),
):
    comment_query = db.query(models.Comments).filter(models.Comments.id == comment_id)
    comment_first = comment_query.first()

    if not comment_first:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"comment with id:{comment_id} not found",
        )

    if comment_first.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform the requested action",
        )

    comment_query.update(comment.model_dump(), synchronize_session=False)
    db.commit()

    return comment_query.first()


# delete a comment
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(ouath2.get_current_user),
):
    comment_query = db.query(models.Comments).filter(models.Comments.id == id)
    comment_first = comment_query.first()

    if not comment_first:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"comment with id:{id} not found",
        )

    if comment_first.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform the requested action",
        )

    comment_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
