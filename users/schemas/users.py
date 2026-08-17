from pydantic import BaseModel, ConfigDict


class Profile(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    company_name: str | None = None
    license_number: str | None = None
    legal_name: str | None = None
    website: str | None = None


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: str
    first_name: str
    last_name: str

    profile: Profile | None = None

    is_active: bool
    is_superuser: bool
    is_verified: bool


class UserCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: str
    first_name: str
    last_name: str


class UserUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None

    is_active: bool | None = None
    is_superuser: bool | None = None
    is_verified: bool | None = None
