from jose import jwt, JWTError, ExpiredSignatureError
import uuid
import logging
from itsdangerous import URLSafeTimedSerializer
from ..config import settings
from datetime import datetime, timedelta
from passlib.context import CryptContext

ACCESS_TOKEN_EXPIRY = 1

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)


def verify(plain_pwd, hash_pwd):
    return pwd_context.verify(plain_pwd, hash_pwd)


def create_access_token(
    user_data: dict, expiry: timedelta = None, refresh: bool = False
):
    payload = {}

    payload["user"] = user_data
    payload["exp"] = datetime.now() + (
        expiry if expiry is not None else timedelta(days=ACCESS_TOKEN_EXPIRY)
    )
    payload["jti"] = str(uuid.uuid4())
    payload["refresh"] = refresh

    token = jwt.encode(
        claims=payload, key=settings.secret_key, algorithm=settings.algorithm
    )
    return token


def decode_token(token: str) -> dict:
    try:
        token_data = jwt.decode(
            token=token, key=settings.secret_key, algorithms=[settings.algorithm]
        )
        return token_data

    except ExpiredSignatureError:
        logging.error("Token expired")
        return None
    except JWTError as e:
        logging.exception(e)
        return None


serializer = URLSafeTimedSerializer(
    secret_key=settings.secret_key, salt="email-configuration"
)
