from redis.asyncio import Redis
from app.config import settings

JTI_EXPIRY = 3600

token_blocklist = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=0,
    decode_responses=True
)


async def add_jti_to_blocklist(jti: str) -> None:
    await token_blocklist.set(name=jti, value="", ex=JTI_EXPIRY)


async def token_in_blocklist(jti: str) -> bool:
    value = await token_blocklist.get(jti)
    return value is not None


async def close_redis():
    await token_blocklist.close()
