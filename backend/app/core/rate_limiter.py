import asyncio
import aioredis

from app.core.config import settings



redis = None

async def get_redis():
    global redis
    if not redis:
        redis = await aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}", decode_responses=True)
    return redis

async def rate_limit(key: str, limit: int = 5, expire: int = 60):
    r = await get_redis()
    count = await r.get(key)
    if count and int(count) >= limit:
        return False
    else:
        pipe = r.pipeline()
        pipe.incr(key)
        pipe.expire(key, expire)
        await pipe.execute()
        return True
