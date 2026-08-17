import uuid
from sqlmodel import Field, Relationship
from models.mixins.timestamps import TimestampMixin


class Profile(TimestampMixin, table=True):
    __tablename__ = "profiles"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id")

    company_name: str | None = Field(default=None)
    license_number: str | None = Field(default=None)
    legal_name: str | None = Field(default=None)
    website: str | None = Field(default=None)

    user: "User" = Relationship(back_populates="profile")
