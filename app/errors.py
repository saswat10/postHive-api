from typing import Any, Callable
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi import FastAPI, status
from sqlalchemy.exc import SQLAlchemyError

class PostHiveException(Exception):
    """This is the base class for all the exceptions"""
    pass

class InvalidToken(PostHiveException):
    """User has provided invalid or expired token"""
    pass

class RevokedToken(PostHiveException):
    pass

class AccessTokenRequired(PostHiveException):
    pass

class RevokedToken(PostHiveException):
    pass

class RefreshTokenRequired(PostHiveException):
    pass

class UserAlreadyExists(PostHiveException):
    pass

class InsufficientPermissions(PostHiveException):
    pass

class PostNotFound(PostHiveException):
    pass


def create_exception_handler(
    status_code: int, initial_detail: Any
) -> Callable[[Request, Exception], JSONResponse]:

    async def exception_handler(request: Request, exc: PostHiveException):
        return JSONResponse(content=initial_detail, status_code=status_code)
    return exception_handler


def register_all_errors(app: FastAPI):
    app.add_exception_handler(
        UserAlreadyExists,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message":"User with email already exists",
                "error_code":"user_exists"
            },
        ),
    )


