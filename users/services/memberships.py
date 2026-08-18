import logging
import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from models.memberships import Membership
from models.users import User
from services.persistence import commit_refresh

logger = logging.getLogger(__name__)


async def get_membership(
    session: AsyncSession,
    developer_id: uuid.UUID,
    builder_id: uuid.UUID,
) -> Membership | None:
    return (
        await session.exec(
            select(Membership).where(
                Membership.developer_id == developer_id,
                Membership.builder_id == builder_id,
            )
        )
    ).first()


async def list_builders(session: AsyncSession, developer_id: uuid.UUID) -> list[User]:
    return list(
        (
            await session.exec(
                select(User)
                .join(Membership, Membership.builder_id == User.id)
                .where(Membership.developer_id == developer_id)
                .order_by(User.email)
            )
        ).all()
    )


async def add_membership(session: AsyncSession, membership: Membership) -> Membership:
    session.add(membership)
    await commit_refresh(session, membership, operation="users.membership.create")
    logger.info(
        f"Membership persisted: developer_id={membership.developer_id}, builder_id={membership.builder_id}"
    )
    return membership
