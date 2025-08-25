from fastapi.exceptions import HTTPException
from fastapi import status
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..entities.comments import Comments
from .models import CommentCreateModel, ParentCommentModel, ReplyModel
from ..auth.service import AuthService
from ..posts.service import PostService

auth_service = AuthService()
post_service = PostService()


class CommentsService:
    async def create_comment(
        self,
        comment: CommentCreateModel,
        post_uid: str,
        user_email: str,
        session: AsyncSession,
    ) -> Comments:
        try:
            post = await post_service.get_post(post_uid, session)
            user = await auth_service.get_user(user_email, session)

            if post is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Post with id:{post_uid} not found"
                )
            
            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"User not found"
                )

            new_comment = Comments(**comment.model_dump())

            new_comment.user = user
            new_comment.post = post

            session.add(new_comment)
            await session.commit()

            return new_comment
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"{e}",
            )
