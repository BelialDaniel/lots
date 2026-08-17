import logging
from collections.abc import Sequence
from typing import Any

from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class PersistenceError(Exception):
    """Raised when a DB commit/refresh fails; map to HTTP in API layer."""

    def __init__(self, detail: str, status_code: int = 500) -> None:
        self.detail = detail
        self.status_code = status_code
        super().__init__(detail)


async def commit_session(session: AsyncSession, *, operation: str) -> None:
    try:
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        logger.exception(f"Integrity error during {operation}")
        raise PersistenceError(
            "A database constraint was violated.",
            status_code=409,
        ) from exc
    except OperationalError as exc:
        await session.rollback()
        logger.exception(f"Operational error during {operation}")
        raise PersistenceError(
            "The database is temporarily unavailable. Please try again.",
            status_code=503,
        ) from exc
    except SQLAlchemyError as exc:
        await session.rollback()
        logger.exception(f"SQLAlchemy error during {operation}")
        raise PersistenceError(
            "An unexpected database error occurred.",
            status_code=500,
        ) from exc


async def commit_refresh(session: AsyncSession, instance: Any, *, operation: str) -> None:
    try:
        await session.commit()
        await session.refresh(instance)
    except IntegrityError as exc:
        await session.rollback()
        logger.exception(f"Integrity error during {operation}")
        raise PersistenceError(
            "A database constraint was violated.",
            status_code=409,
        ) from exc
    except OperationalError as exc:
        await session.rollback()
        logger.exception(f"Operational error during {operation}")
        raise PersistenceError(
            "The database is temporarily unavailable. Please try again.",
            status_code=503,
        ) from exc
    except SQLAlchemyError as exc:
        await session.rollback()
        logger.exception(f"SQLAlchemy error during {operation}")
        raise PersistenceError(
            "An unexpected database error occurred.",
            status_code=500,
        ) from exc


async def commit_refresh_many(session: AsyncSession, instances: Sequence[Any], *, operation: str) -> None:
    try:
        await session.commit()
        for instance in instances:
            await session.refresh(instance)
    except IntegrityError as exc:
        await session.rollback()
        logger.exception(f"Integrity error during {operation}")
        raise PersistenceError(
            "A database constraint was violated.",
            status_code=409,
        ) from exc
    except OperationalError as exc:
        await session.rollback()
        logger.exception(f"Operational error during {operation}")
        raise PersistenceError(
            "The database is temporarily unavailable. Please try again.",
            status_code=503,
        ) from exc
    except SQLAlchemyError as exc:
        await session.rollback()
        logger.exception(f"SQLAlchemy error during {operation}")
        raise PersistenceError(
            "An unexpected database error occurred.",
            status_code=500,
        ) from exc
