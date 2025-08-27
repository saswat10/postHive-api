from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from .models import VoteModel
from .service import VoteService
from ..comments.service import CommentsService
from ..posts.service import PostService

from ..auth.dependencies import AccessTokenBearer, get_session

vote_router = APIRouter()
vote_service = VoteService()
post_service = PostService()
comment_service = CommentsService()
access_token_bearer = AccessTokenBearer()


@vote_router.post("/post/{post_uid}")
async def vote_on_post(
    post_uid: str,
    vote: VoteModel,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
):
    post = await post_service.get_post(post_uid, session)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    try:
        result = await vote_service.vote_post(
            session=session,
            target_uid=post_uid,
            user_uid= token_details.get('user')['user_uid'],
            value=vote.value,
        )
        return {"message": "Vote recorded", "result": result}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@vote_router.post("/comment/{comment_uid}")
async def vote_on_comment(
    comment_uid: str,
    vote: VoteModel,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
):
    comment = await comment_service.get_comment(comment_uid, session)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )

    try:
        result = await vote_service.vote_comment(
            session=session,
            target_uid=comment_uid,
            user_uid=token_details.get('user')['user_uid'],
            value=vote.value,
        )
        return {"message": "Vote recorded", "result": result}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
