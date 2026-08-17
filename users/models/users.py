import uuid
from models.mixins.timestamps import TimestampMixin
from sqlmodel import Field, Relationship


class User(TimestampMixin, table=True):
    __tablename__ = "users"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(unique=True, nullable=False)

    first_name: str = Field(nullable=False)
    last_name: str = Field(nullable=False)

    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    is_verified: bool = Field(default=False)

    profile: "Profile" = Relationship(back_populates="user")
