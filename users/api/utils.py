import uuid
from fastapi import Header, HTTPException, status

from api.headers import USER_ID


async def get_current_user_id(x_user_id: str = Header(..., alias=USER_ID)) -> uuid.UUID:
    try:
        return uuid.UUID(x_user_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user id",
        ) from exc
