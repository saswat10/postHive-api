from fastapi.exceptions import HTTPException
from fastapi import status
from sqlmodel import select
from sqlalchemy.orm import selectinload
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
                    detail=f"Post with id:{post_uid} not found",
                )

            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail=f"User not found"
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

    async def get_comment(self, comment_uid: str, session: AsyncSession):
        result = await session.execute(
            select(Comments)
            .options(
                selectinload(Comments.post),       # preload post
                selectinload(Comments.replies),    # preload replies if needed
            )
            .where(Comments.uid == comment_uid)
        )
        comment = result.scalars().first()
        if not comment:
            raise Exception("Comment not found")
        return comment

    async def get_comments_for_post(
        self, post_uid: str, session: AsyncSession
    ) -> list[Comments]:
        result = await session.execute(
            select(Comments).where(Comments.post_uid == post_uid)
        )
        return result.scalars().all()
    
    async def update_comment(
        self, comment_uid: str, content: str, user_email: str, session: AsyncSession
    ) -> Comments:
        comment = await self.get_comment(comment_uid, session)
        user = await auth_service.get_user(user_email, session)

        if comment.user_uid != user.uid:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to edit this comment"
            )

        comment.content = content
        await session.commit()
        await session.refresh(comment)
        return comment
    
    async def delete_comment(
        self, comment_uid: str, user_email: str, session: AsyncSession
    ) -> dict:
        comment = await self.get_comment(comment_uid, session)
        user = await auth_service.get_user(user_email, session)

        if comment.user_uid != user.uid:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this comment"
            )

        await session.delete(comment)
        await session.commit()
        return {"detail": f"Comment {comment_uid} deleted successfully"}


    async def reply_to_comment(
        self,
        comment_uid: str,
        reply: ReplyModel,
        user_email: str,
        session: AsyncSession,
    ) -> Comments:
        parent = await self.get_comment(comment_uid, session)
        user = await auth_service.get_user(user_email, session)

        new_reply = Comments(**reply.model_dump())
        new_reply.user = user
        new_reply.post = parent.post
        new_reply.parent_comment = parent

        session.add(new_reply)
        await session.commit()
        await session.refresh(new_reply)
        return new_reply
