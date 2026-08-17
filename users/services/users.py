import logging

from sqlalchemy.ext.asyncio import AsyncSession

from models.users import User
from services.persistence import commit_refresh

logger = logging.getLogger(__name__)


async def create_user(session: AsyncSession, user: User) -> User:
    session.add(user)
    await commit_refresh(session, user, operation="users.user.create")
    logger.info(f"User persisted: email={user.email}, id={user.id}")
    return user


async def update_user(session: AsyncSession, user: User) -> User:
    await commit_refresh(session, user, operation="users.user.update")
    logger.info(f"User update persisted: id={user.id}")
    return user
