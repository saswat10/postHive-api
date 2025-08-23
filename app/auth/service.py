from pydantic import EmailStr

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc

from ..entities.user import User
from .models import UserCreateModel
from ..utils import hash, verify

class AuthService:
    async def get_user(self, email: EmailStr, session: AsyncSession):
        statement = select(User).where(User.email == email)
        result = await session.exec(statement)
        return result.first()
    
    
    async def user_exists(self, email: EmailStr, session: AsyncSession):
        user = await self.get_user(email, session)
        return True if user is not None else False
    

    async def create_user(self, user_data: UserCreateModel, session: AsyncSession):
        user_data_dict = user_data.model_dump()

        new_user = User(
            **user_data_dict
        )
        new_user.password = hash(user_data_dict['password'])
        session.add(new_user)
        await session.commit()
        return new_user

