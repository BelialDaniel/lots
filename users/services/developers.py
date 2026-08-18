import logging
import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from models.developers import Developer
from services.persistence import commit_refresh

logger = logging.getLogger(__name__)


async def get_developer_by_id(session: AsyncSession, developer_id: uuid.UUID) -> Developer | None:
    return (await session.exec(select(Developer).where(Developer.id == developer_id))).first()


async def get_developer_by_slug(session: AsyncSession, slug: str) -> Developer | None:
    return (await session.exec(select(Developer).where(Developer.slug == slug))).first()


async def create_developer(session: AsyncSession, developer: Developer) -> Developer:
    session.add(developer)
    await commit_refresh(session, developer, operation="users.developer.create")
    logger.info(f"Developer persisted: slug={developer.slug}, id={developer.id}")
    return developer
