from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from ..entities.votes import Votes
from datetime import datetime


class VoteService:
    async def vote(
        self,
        target_type: str,
        target_uid: str,
        user_uid: str,
        value: int,
        session: AsyncSession,
    ):
        statement = select(Votes).where(
            Votes.user_uid == user_uid,
            Votes.target_type == target_type,
            Votes.target_uid == target_uid
        )
        result = await session.execute(statement)
        existing_vote = result.scalars().one_or_none()

        if existing_vote:
            existing_vote.vote = value
            existing_vote.updated_at = datetime.now()
            vote = existing_vote
        else:
            vote = Votes(
                user_uid=user_uid,
                target_uid=target_uid,
                target_type=target_type,
                vote=value,
            )
            session.add(vote)

        await session.commit()
        await session.refresh(vote)
        return vote

    async def vote_post(
        self, target_uid: str, user_uid: str, value: int, session: AsyncSession
    ):
        post_vote = await self.vote("post", target_uid, user_uid, value, session)
        return post_vote

    async def vote_comment(
        self, target_uid: str, user_uid: str, value: int, session: AsyncSession
    ):
        comment_vote = await self.vote("comment", target_uid, user_uid, value, session)
        return comment_vote
