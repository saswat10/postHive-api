from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from .service import AuthService
from .models import UserCreateModel, UserModel
from ..db.main import get_session

auth_router = APIRouter()
auth_service =  AuthService()

@auth_router.post("/signup", response_model=UserModel)
async def create_user_account(user_data: UserCreateModel, session: AsyncSession = Depends(get_session)):
    email = user_data.email
    user_exists = await auth_service.user_exists(email, session)
    
    if user_exists:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User with email already exists")
    
    new_user = await auth_service.create_user(user_data, session)
    return new_user
