import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.utils import get_current_user_id
from core.database import get_session
from models.developers import Developer
from models.memberships import Membership
from schemas.developers import (
    AddBuilderRequest,
    BuilderResponse,
    DeveloperCreate,
    DeveloperResponse,
)
from services.developers import create_developer, get_developer_by_id, get_developer_by_slug
from services.memberships import add_membership, get_membership, list_builders
from services.users import get_user_by_email, get_user_by_id

router = APIRouter(prefix="/api/v1/users/developers", tags=["users:developers"])


async def _owned_developer(
    session: AsyncSession,
    developer_id: uuid.UUID,
    user_id: uuid.UUID,
) -> Developer:
    developer = await get_developer_by_id(session, developer_id)
    if developer is None:
        raise HTTPException(status_code=404, detail="Developer not found")
    if developer.owner_user_id != user_id:
        raise HTTPException(status_code=403, detail="Not the owner of this developer")
    return developer


@router.post("/", response_model=DeveloperResponse, status_code=201)
async def create_developer_api(
    body: DeveloperCreate,
    user_id: uuid.UUID = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
) -> Developer:
    owner = await get_user_by_id(session, user_id)
    if owner is None:
        raise HTTPException(status_code=404, detail="User not found")

    existing = await get_developer_by_slug(session, body.slug)
    if existing is not None:
        raise HTTPException(status_code=409, detail="Slug already taken")

    developer = Developer(slug=body.slug, owner_user_id=user_id)
    return await create_developer(session, developer)


@router.post("/{developer_id}/builders", response_model=BuilderResponse, status_code=201)
async def add_builder_api(
    developer_id: uuid.UUID,
    body: AddBuilderRequest,
    user_id: uuid.UUID = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
) -> BuilderResponse:
    await _owned_developer(session, developer_id, user_id)

    builder = await get_user_by_email(session, body.email)
    if builder is None:
        raise HTTPException(status_code=404, detail="User not found")

    if builder.id == user_id:
        raise HTTPException(status_code=400, detail="Owner cannot be added as a builder")

    existing = await get_membership(session, developer_id, builder.id)
    if existing is not None:
        raise HTTPException(status_code=409, detail="Builder already belongs to this developer")

    await add_membership(
        session,
        Membership(developer_id=developer_id, builder_id=builder.id),
    )
    return builder


@router.get("/{developer_id}/builders", response_model=list[BuilderResponse])
async def list_builders_api(
    developer_id: uuid.UUID,
    user_id: uuid.UUID = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
) -> list[BuilderResponse]:
    await _owned_developer(session, developer_id, user_id)
    return await list_builders(session, developer_id)
