from fastapi import APIRouter, Depends, HTTPException, status
from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from .models import CommentCreateModel, ParentCommentModel
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
