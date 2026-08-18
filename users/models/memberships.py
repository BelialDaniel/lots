import uuid
from sqlalchemy import UniqueConstraint
from sqlmodel import Field, Relationship
from models.mixins.timestamps import TimestampMixin


class Membership(TimestampMixin, table=True):
    __tablename__ = "memberships"
    __table_args__ = (
        UniqueConstraint("developer_id", "builder_id", name="uq_membership_developer_builder"),
    )

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    developer_id: uuid.UUID = Field(foreign_key="developers.id", index=True, nullable=False)
    builder_id: uuid.UUID = Field(foreign_key="users.id", index=True, nullable=False)

    developer: "Developer" = Relationship(back_populates="memberships")
