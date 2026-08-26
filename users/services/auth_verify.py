import logging
import uuid

import httpx
from fastapi import HTTPException, status

from api.headers import USER_ID
from core.config import settings

logger = logging.getLogger(__name__)

_client: httpx.AsyncClient | None = None


def init_auth_client() -> None:
    global _client
    _client = httpx.AsyncClient(timeout=httpx.Timeout(5.0), follow_redirects=False)


async def close_auth_client() -> None:
    global _client
    if _client is not None:
        await _client.aclose()
        _client = None


async def verify_user_id(*, cookie: str | None, authorization: str | None) -> uuid.UUID:
    if _client is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Identity client is not ready",
        )

    headers: dict[str, str] = {}
    if cookie:
        headers["Cookie"] = cookie
    if authorization:
        headers["Authorization"] = authorization

    try:
        response = await _client.get(settings.AUTH_VERIFY_URL, headers=headers)
    except httpx.RequestError as exc:
        logger.exception("auth /verify unreachable")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Identity service unavailable",
        ) from exc

    if response.status_code == status.HTTP_401_UNAUTHORIZED:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    if response.status_code != status.HTTP_200_OK:
        logger.error("auth /verify unexpected status %s", response.status_code)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Identity verification failed",
        )

    raw_user_id = response.headers.get(USER_ID)
    if not raw_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    try:
        return uuid.UUID(raw_user_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        ) from exc
