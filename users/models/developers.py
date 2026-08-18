import uuid
from sqlmodel import Field, Relationship
from models.mixins.timestamps import TimestampMixin


class Developer(TimestampMixin, table=True):
    __tablename__ = "developers"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    slug: str = Field(unique=True, index=True, nullable=False, max_length=63)
    owner_user_id: uuid.UUID = Field(foreign_key="users.id", index=True, nullable=False)

    memberships: list["Membership"] = Relationship(back_populates="developer")
