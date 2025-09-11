from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc,func
from fastapi import HTTPException, status
from ..entities import Moderator

from .models import CreateModeratorModel, ModeratorModel
from ..auth.service import AuthService


auth_service = AuthService()


class ModeratorService:
    async def create_admin(self, moderator: CreateModeratorModel, session: AsyncSession):
        try:    
            moderator_dict = moderator.model_dump()
            new_moderator = Moderator(**moderator_dict)
            session.add(new_moderator)
            await session.commit()

            return new_moderator        
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

        