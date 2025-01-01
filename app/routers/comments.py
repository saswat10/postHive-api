from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, ouath2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func

router = APIRouter(prefix="/comments", tags=["Comments"])



@router.put("/{comment_id}", response_model=schemas.Comment)
def update_comment(comment_id: int, updated_comment: schemas.CommentCreate,
                  db: Session = Depends(get_db),
                  current_user = Depends(ouath2.get_current_user)):
    comment_query = db.query(models.Comments).filter(models.Comments.id == comment_id)
    comment = comment_query.first()
    
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to perform action")
        
    comment_query.update(updated_comment.dict(), synchronize_session=False)
    db.commit()
    return comment_query.first()

@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(comment_id: int, db: Session = Depends(get_db),
                  current_user = Depends(ouath2.get_current_user)):
    comment_query = db.query(models.Comments).filter(models.Comments.id == comment_id)
    comment = comment_query.first()
    
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to perform action")
        
    comment_query.delete(synchronize_session=False)
    db.commit()
    return