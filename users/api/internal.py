import logging
import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.utils import get_current_user_id
from core.database import get_session
from models.utils.slugs import normalize_slug
from schemas.developers import TenantResolveResponse, TenantRole
from services.developers import get_developer_by_slug
from services.memberships import get_membership

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/users/internal", tags=["users:internal"])


@router.get("/tenants/{slug}", response_model=TenantResolveResponse)
async def resolve_tenant(
    slug: str,
    user_id: uuid.UUID = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
) -> TenantResolveResponse:
    developer = await get_developer_by_slug(session, normalize_slug(slug))
    if developer is None:
        raise HTTPException(status_code=404, detail="Developer not found")

    if developer.owner_user_id == user_id:
        return TenantResolveResponse(
            developer_id=developer.id,
            slug=developer.slug,
            role=TenantRole.DEVELOPER,
        )

    membership = await get_membership(session, developer.id, user_id)
    if membership is None:
        raise HTTPException(status_code=403, detail="Not a member of this developer")

    return TenantResolveResponse(
        developer_id=developer.id,
        slug=developer.slug,
        role=TenantRole.BUILDER,
    )
