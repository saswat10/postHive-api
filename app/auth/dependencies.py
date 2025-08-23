from fastapi import Request, status, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel.ext.asyncio.session import AsyncSession
from .utils import decode_token
from ..db.redis import token_in_blocklist
from ..db.main import get_session
from ..entities.user import User
from .service import AuthService
from typing import List


authService = AuthService()


class TokenBearer(HTTPBearer):
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> dict | None:
        creds: HTTPAuthorizationCredentials = await super().__call__(request)

        token = creds.credentials
        token_data = decode_token(token)

        if token_data is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid or expired token"
            )

        if await token_in_blocklist(token_data['jti']):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error":"This token is invalid or has been revoked",
                    "resolution": "Please get new token"
                }
            )

        self.verify_token_data(token_data)

        return token_data
    
    def verify_token_data(self, token_data):
        raise NotImplementedError("Please override this method in the child classes")


class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict)->None:
        if token_data and token_data['refresh']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide access token"
            )


class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict)->None:
        if token_data and not token_data['refresh']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide refresh token"
            )


async def get_current_user(
    token_details: dict = Depends(AccessTokenBearer()),
    session: AsyncSession = Depends(get_session)
):
    email = token_details["user"]["email"]
    user = await authService.get_user(email=email, session=session)
    return user
    

class RoleChecker:
    def __init__(self, allowed_roles: List[str])->None:

        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)):
        
        if current_user.role in self.allowed_roles:
            return True
        
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not permitted to perform this operation"
        )

        