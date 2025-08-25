from fastapi import APIRouter, Depends, HTTPException, status
from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from .models import CommentCreateModel, ParentCommentModel, ReplyModel
from ..db.main import get_session
from .service import CommentsService
from ..entities.user import User

from ..auth.dependencies import get_current_user

comments_router = APIRouter()
comments_service = CommentsService()


@comments_router.post(
    "/{post_uid}",
    response_model=ParentCommentModel,
    status_code=status.HTTP_201_CREATED,
)
async def create_comment(
    comment: CommentCreateModel,
    post_uid: str,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return await comments_service.create_comment(
        comment, post_uid, current_user.email, session
    )


@comments_router.post(
    "/reply/{comment_uid}",
    response_model=ParentCommentModel,
    status_code=status.HTTP_201_CREATED,
)
async def add_reply(
    reply: CommentCreateModel,
    comment_uid: str,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return await comments_service.reply_to_comment(
        comment_uid, reply, current_user.email, session
    )

@comments_router.put(
    "/{comment_uid}",
    response_model=ParentCommentModel,
    status_code=status.HTTP_200_OK,
)
async def update_comment(
    comment_uid: str,
    updated_comment: CommentCreateModel,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return await comments_service.update_comment(
        comment_uid, updated_comment, current_user.email, session
    )

@comments_router.delete(
    "/{comment_uid}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_comment(
    comment_uid: str,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return await comments_service.delete_comment(
        comment_uid, current_user.email, session
    )
