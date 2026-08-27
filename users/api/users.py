import uuid

from fastapi import APIRouter, Depends, HTTPException
from core.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from services.users import create_user, get_user_by_id, update_user
from services.profile import save_new_profile

from models.users import User
from models.profile import Profile
from schemas.users import UserCreate, UserResponse, UserUpdate
from api.utils import get_current_user_id

router = APIRouter(prefix="/api/v1/users", tags=["users:user"])


@router.get("/me", response_model=UserResponse)
async def get_me(
    user_id: uuid.UUID = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
) -> User:
    user = await get_user_by_id(session, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


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

    await create_user(session, new_user)
    await save_new_profile(session, Profile(user_id=new_user.id))
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

    await update_user(session, user)
    return user
