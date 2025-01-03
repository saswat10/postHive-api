from fastapi import FastAPI, Response, status, HTTPException, APIRouter, Depends
from .. import schemas, database, models, ouath2
from sqlalchemy.orm import Session

router = APIRouter(prefix="/vote", tags=["Vote"])


# @router.post("/", status_code=status.HTTP_201_CREATED)
# def vote(
#     vote: schemas.Vote,
#     db: Session = Depends(database.get_db),
#     current_user: int = Depends(ouath2.get_current_user),
# ):
#     post = (
#         db.query(models.Post).filter(models.Post.id == vote.post_id)
#     )
#     print(post)
#     print("LIEN18")
#     if not post.first():
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Post with id: {vote.post_id} not found",
#         )

#     vote_query = db.query(models.Vote).filter(
#         models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id
#     )
#     print(vote_query)
#     print('LINE25')
#     found_vote = vote_query.first()

#     if vote.dir == 1:
#         if found_vote:
#             raise HTTPException(
#                 status_code=status.HTTP_409_CONFLICT,
#                 detail=f"user {current_user.id} has already voted on post {vote.post_id}",
#             )
#         new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
#         db.add(new_vote)
#         db.commit()
#         return {"message": "successfully added vote"}
#     else:
#         if not found_vote:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND, detail="vote doesn't exist"
#             )
#         vote_query.delete(synchronize_session=False)
#         db.commit()

#         return {"message": "successfully deleted voted"}


@router.post("/{post_id}")
def vote(post_id: int, db: Session = Depends(database.get_db), 
         current_user = Depends(ouath2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
        
    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == post_id, models.Vote.user_id == current_user.id
    )
    found_vote = vote_query.first()
    
    if found_vote:
        vote_query.delete()
        db.commit()
        return {"message": "Vote removed"}
    
    new_vote = models.Vote(post_id=post_id, user_id=current_user.id)
    db.add(new_vote)
    db.commit()
    return {"message": "Vote added"}