from fastapi import HTTPException, Request, status

from app.core.in_mem_rate_limiter import InMemoryRateLimiter


LIMIT = 5 # requests per window
WINDOW = 30 # seconds

rate_limiter = InMemoryRateLimiter()


async def rate_limit_dependency(request: Request):
    key = request.client.host
    allowed = rate_limiter.rate_limit(key, limit=LIMIT, window=WINDOW)

    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests"
        )

