import logging

from sqlalchemy.ext.asyncio import AsyncSession

from models.profile import Profile
from services.persistence import commit_refresh

logger = logging.getLogger(__name__)


async def save_new_profile(session: AsyncSession, profile: Profile) -> Profile:
    session.add(profile)
    await commit_refresh(session, profile, operation="users.profile.create")
    logger.info(f"Profile persisted: id={profile.id}")
    return profile


async def update_profile(session: AsyncSession, profile: Profile) -> Profile:
    await commit_refresh(session, profile, operation="users.profile.update")
    logger.info(f"Profile update persisted: id={profile.id}")
    return profile
