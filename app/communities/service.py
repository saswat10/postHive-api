from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc,func
from fastapi import HTTPException, status

from ..entities.communities import Communities
from .models import CommunityCreateModel, CommunityModel
from ..auth.dependencies import get_current_user
from ..auth.service import AuthService

import re
import unicodedata


auth_service = AuthService()


class CommunityService:
    async def create_new_community(self, community: CommunityCreateModel, user_email: str, session: AsyncSession):
        try:    
            user = await auth_service.get_user(email=user_email, session=session)
            
            community_exists = await self.get_community(name=community.name, session=session)
            if community_exists:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Community with community name:{community.name} already exists",
                )
            
            community_data_dict = community.model_dump()
            new_community = Communities(**community_data_dict)
            new_community.slug = self.create_slug(new_community.name)
            new_community.creator = user

            session.add(new_community)
            await session.commit()

            return new_community
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

        
    async def get_community(self, name: str, session: AsyncSession):
        name = name.lower()
        statement = (
            select(Communities)
            .where(func.lower(Communities.name) == name)
        )
        result = await session.exec(statement=statement)
        community = result.first()
        return community if community else None

    async def get_communities(self, session: AsyncSession):
        statement = select(Communities).order_by(desc(Communities.updated_at))
        result = await session.exec(statement)
        return result.all()
    

    def create_slug(self, name: str)->str:
        name = unicodedata.normalize("NFKD", name)
        name = name.encode("ascii", "ignore").decode("ascii")
    
        name = name.lower()
    

        name = re.sub(r"[^a-z0-9]+", "-", name)
        name = name.strip("-")
    
        return name