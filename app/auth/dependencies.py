from fastapi import Request, status, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .utils import decode_token

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
