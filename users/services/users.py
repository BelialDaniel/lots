import logging
import uuid

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from models.users import User
from services.persistence import commit_refresh

logger = logging.getLogger(__name__)


async def get_user_by_id(session: AsyncSession, user_id: uuid.UUID) -> User | None:
    return (await session.exec(select(User).where(User.id == user_id))).first()


async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
    return (
        await session.exec(select(User).where(func.lower(User.email) == email.lower()))
    ).first()


async def create_user(session: AsyncSession, user: User) -> User:
    session.add(user)
    await commit_refresh(session, user, operation="users.user.create")
    logger.info(f"User persisted: email={user.email}, id={user.id}")
    return user


async def update_user(session: AsyncSession, user: User) -> User:
    await commit_refresh(session, user, operation="users.user.update")
    logger.info(f"User update persisted: id={user.id}")
    return user
