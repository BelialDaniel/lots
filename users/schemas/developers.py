import uuid
from enum import Enum

from pydantic import BaseModel, ConfigDict, field_validator

from models.utils.slugs import validate_slug


class TenantRole(str, Enum):
    DEVELOPER = "developer"
    BUILDER = "builder"


class DeveloperCreate(BaseModel):
    slug: str

    @field_validator("slug")
    @classmethod
    def slug_must_be_valid(cls, value: str) -> str:
        return validate_slug(value)


class DeveloperResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    slug: str
    owner_user_id: uuid.UUID


class AddBuilderRequest(BaseModel):
    email: str

    @field_validator("email")
    @classmethod
    def email_must_be_present(cls, value: str) -> str:
        email = value.strip().lower()
        if not email:
            raise ValueError("Email is required")
        return email


class BuilderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    email: str
    first_name: str
    last_name: str


class TenantResolveResponse(BaseModel):
    developer_id: uuid.UUID
    slug: str
    role: TenantRole
