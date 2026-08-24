import logging

from fastapi import Request
from fastapi.responses import JSONResponse

from services.persistence import PersistenceError

logger = logging.getLogger(__name__)


async def persistence_error_handler(_request: Request, exc: PersistenceError) -> JSONResponse:
    logger.error("Persistence error: %s", exc.detail)
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
