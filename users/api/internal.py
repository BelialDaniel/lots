import logging
import uuid

from fastapi import APIRouter, Depends, Header, HTTPException, Request, Response
from sqlmodel.ext.asyncio.session import AsyncSession

from api.headers import DEVELOPER_ID, TENANT_SLUG, USER_ID, USER_ROLE
from api.utils import get_current_user_id
from core.database import get_session
from models.developers import Developer
from models.utils.slugs import normalize_slug
from schemas.developers import TenantResolveResponse, TenantRole
from services.auth_verify import verify_user_id
from services.developers import get_developer_by_slug
from services.memberships import get_membership

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/users/internal", tags=["users:internal"])


async def _role_in_developer(session: AsyncSession, developer: Developer, user_id: uuid.UUID) -> TenantRole | None:
    if developer.owner_user_id == user_id:
        return TenantRole.DEVELOPER

    membership = await get_membership(session, developer.id, user_id)
    if membership is None:
        return None
    return TenantRole.BUILDER


@router.get("/access", include_in_schema=False)
async def check_access(
    request: Request,
    x_tenant_slug: str | None = Header(default=None, alias=TENANT_SLUG),
    session: AsyncSession = Depends(get_session),
) -> Response:
    user_id = await verify_user_id(
        cookie=request.headers.get("cookie"),
        authorization=request.headers.get("authorization"),
    )

    headers = {USER_ID: str(user_id)}
    slug = (x_tenant_slug or "").strip()
    if not slug:
        return Response(status_code=200, headers=headers)

    developer = await get_developer_by_slug(session, normalize_slug(slug))
    if developer is None:
        logger.info("access denied: unknown slug=%s user_id=%s", slug, user_id)
        raise HTTPException(status_code=403, detail="Not a member of this developer")

    role = await _role_in_developer(session, developer, user_id)
    if role is None:
        logger.info("access denied: not a member slug=%s user_id=%s", slug, user_id)
        raise HTTPException(status_code=403, detail="Not a member of this developer")

    headers[DEVELOPER_ID] = str(developer.id)
    headers[USER_ROLE] = role.value
    return Response(status_code=200, headers=headers)


@router.get("/tenants/{slug}", response_model=TenantResolveResponse)
async def resolve_tenant(
    slug: str,
    user_id: uuid.UUID = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
) -> TenantResolveResponse:
    developer = await get_developer_by_slug(session, normalize_slug(slug))
    if developer is None:
        raise HTTPException(status_code=404, detail="Developer not found")

    role = await _role_in_developer(session, developer, user_id)
    if role is None:
        raise HTTPException(status_code=403, detail="Not a member of this developer")

    return TenantResolveResponse(
        developer_id=developer.id,
        slug=developer.slug,
        role=role,
    )
