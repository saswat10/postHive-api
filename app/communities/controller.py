from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from .models import CommunityCreateModel, CommunityModel
from ..db.main import get_session
from .service import CommunityService
from ..entities.user import User

from ..auth.dependencies import get_current_user

community_service = CommunityService()
community_router = APIRouter()


@community_router.post(
    "/", response_model=CommunityModel, status_code=status.HTTP_201_CREATED
)
async def create_new_community(
    community: CommunityCreateModel,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    return await community_service.create_new_community(
        community=community, user_email=current_user.email, session=session
    )


@community_router.get(
    "/", response_model=List[CommunityModel], status_code=status.HTTP_200_OK
)
async def get_all_communities(session: AsyncSession = Depends(get_session)):
    return await community_service.get_communities(session=session)


@community_router.get("/{name}", response_model=CommunityModel, status_code=status.HTTP_200_OK)
async def get_community(name: str, session: AsyncSession = Depends(get_session)):
    return await community_service.get_community(name=name, session=session)

@community_router.post("/join/{community_name}", status_code=status.HTTP_201_CREATED)
async def join_community():
    pass

