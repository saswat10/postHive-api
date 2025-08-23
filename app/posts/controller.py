from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from .service import PostService
from .models import Post, PostCreateModel, PostUpdateModel
from ..db.main import get_session
from ..auth.dependencies import AccessTokenBearer

post_router = APIRouter()
post_service = PostService()
access_token_bearer = AccessTokenBearer()


@post_router.get("/", response_model=List[Post], status_code=status.HTTP_200_OK)
async def get_all_posts(
    session: AsyncSession = Depends(get_session), _: dict = Depends(access_token_bearer)
):
    return await post_service.get_all_posts(session)


@post_router.get("/{post_uid}", response_model=Post, status_code=status.HTTP_200_OK)
async def get_post(
    post_uid: str,
    session: AsyncSession = Depends(get_session),
    _: dict = Depends(access_token_bearer)
):
    post = await post_service.get_post(post_uid, session)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    return post


@post_router.post("/", response_model=Post, status_code=status.HTTP_201_CREATED)
async def create_post(
    post_data: PostCreateModel,
    session: AsyncSession = Depends(get_session),
    _: dict = Depends(access_token_bearer)
):
    return await post_service.create_post(post_data, session)


@post_router.put("/{post_uid}", response_model=Post, status_code=status.HTTP_200_OK)
async def update_post(
    post_uid: str,
    update_data: PostUpdateModel,
    session: AsyncSession = Depends(get_session),
    _: dict = Depends(access_token_bearer)
):
    updated = await post_service.update_post(post_uid, update_data, session)
    if updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    return updated


@post_router.delete("/{post_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_uid: str,
    session: AsyncSession = Depends(get_session),
    _: dict = Depends(access_token_bearer)
):
    deleted = await post_service.delete_post(post_uid, session)
    if deleted is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    return None  # 204 means no response body
