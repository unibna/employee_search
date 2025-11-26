import time
from threading import Lock
from typing import Dict, List


class InMemoryRateLimiter:
    """
    A simple in-memory rate limiter for demo purposes.

    IMPORTANT:
    - This implementation stores all timestamps in process memory.
    - It only works correctly when the app runs on a single instance.
    - In real production, rate limiting **must be implemented using Redis or
        a distributed cache** so that all instances of the service share the
        same rate-limit state.

    Recommended real-world alternatives:
    - Redis sorted sets (ZADD/ZREMRANGEBYSCORE)
    - API Gateway (Cloudflare, NGINX, Kong, AWS API Gateway)
    """

    def __init__(self):
        self.cache: Dict[str, List[float]] = {}
        self.lock = Lock()

    def rate_limit(self, key: str, limit: int, window: int) -> bool:
        now = time.time()

        with self.lock:
            if key not in self.cache:
                self.cache[key] = []

            self.cache[key].append(now)

            self.cache[key] = [t for t in self.cache[key] if t > now - window]

            return len(self.cache[key]) <= limit

