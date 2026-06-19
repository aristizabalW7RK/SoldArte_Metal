import time
from collections import defaultdict
from fastapi import HTTPException, Request
from backend.core.config import settings


class RateLimiter:
    def __init__(self, max_requests: int = 5, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._attempts: dict[str, list[float]] = defaultdict(list)

    def __call__(self, request: Request):
        if settings.DEBUG:
            return
        key = request.client.host if request.client else "unknown"
        now = time.time()
        window_start = now - self.window_seconds
        self._attempts[key] = [t for t in self._attempts[key] if t > window_start]
        if len(self._attempts[key]) >= self.max_requests:
            raise HTTPException(
                status_code=429,
                detail="Demasiados intentos. Intenta de nuevo en 1 minuto.",
            )
        self._attempts[key].append(now)


rate_limit_login = RateLimiter(max_requests=5, window_seconds=60)
