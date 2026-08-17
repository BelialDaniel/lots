import logging
import uuid

from fastapi import APIRouter, Depends, HTTPException
from core.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from services.users import create_user, update_user
from services.profile import save_new_profile
from services.persistence import PersistenceError

from models.users import User
from models.profile import Profile
from schemas.users import UserCreate, UserResponse, UserUpdate
from api.utils import get_current_user_id

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/users", tags=["users:user"])


@router.post("/", response_model=UserResponse)
async def create_user_api(body: UserCreate, session: AsyncSession = Depends(get_session)) -> UserResponse:
    existing_user = await session.exec(
        select(User).where(User.email == body.email)
    ).escalar_one_or_none()

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = User(
        email=body.email,
        first_name=body.first_name,
        last_name=body.last_name,
        is_superuser=True,
        is_active=True,
    )

    try:
        await create_user(session, new_user)
        await save_new_profile(session, Profile(user_id=new_user.id))
    except PersistenceError as e:
        logger.error(f"Error creating user: {e}")
        raise HTTPException(status_code=e.status_code, detail=e.detail)

    return new_user


@router.put("/", response_model=UserResponse)
async def update_user_api(
    body: UserUpdate,
    user_id: uuid.UUID = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session)
) -> UserResponse:
    user = await session.exec(
        select(User).where(User.id == user_id)
    ).escalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    updates = body.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(user, field, value)

    try:
        await update_user(session, user)
    except PersistenceError as e:
        logger.error(f"Error updating user: {e}")
        raise HTTPException(status_code=e.status_code, detail=e.detail)

    return user