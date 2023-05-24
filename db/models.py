from datetime import datetime
import uuid
from db.schema import Base
import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.sql import func


class User(Base):
    __tablename__ = 'users'

    id: so.Mapped[uuid.UUID] = so.mapped_column(sa.UUID(), primary_key=True, default=uuid.uuid4, nullable=False)
    created_at: so.Mapped[datetime] = so.mapped_column(sa.DateTime(timezone=True), server_default=func.now(), nullable=True)

    email: so.Mapped[str] = so.mapped_column(sa.String(), unique=True, nullable=False)
    password_hash: so.Mapped[str] = so.mapped_column(sa.String(), nullable=False)

    log_groups = so.relationship(
        "LogGroup",
        back_populates='user', lazy='selectin', cascade="all,delete"
    )

    def __repr__(self) -> str:
        return f'{self.email} ({self.id})'


class LogGroup(Base):
    __tablename__ = 'log_group'

    id: so.Mapped[uuid.UUID] = so.mapped_column(sa.UUID(), primary_key=True, default=uuid.uuid4, nullable=False)
    created_at: so.Mapped[datetime] = so.mapped_column(sa.DateTime(timezone=True), server_default=func.now(), nullable=True)

    name: so.Mapped[str] = so.mapped_column(sa.String(), unique=True, nullable=False)
    description: so.Mapped[str] = so.mapped_column(sa.String(), nullable=True)

    log_items = so.relationship(
        "LogItem",
        back_populates='log_group', lazy='selectin', cascade="all,delete"
    )

    user: so.Mapped[User] = so.relationship(back_populates='log_groups', lazy='selectin')
    user_id = so.mapped_column(sa.ForeignKey('users.id'), nullable=False)

    def __repr__(self) -> str:
        return f'{self.name} ({self.id})'


class LogLevel(Base):
    __tablename__ = 'log_level'

    created_at: so.Mapped[datetime] = so.mapped_column(sa.DateTime(timezone=True), server_default=func.now(), nullable=True)

    name: so.Mapped[str] = so.mapped_column(sa.String(), primary_key=True, nullable=False)

    log_items = so.relationship(
        "LogItem",
        back_populates='log_level', lazy='selectin'
    )

    def __repr__(self) -> str:
        return f'{self.name}'


class LogItem(Base):
    __tablename__ = 'log_item'

    id: so.Mapped[uuid.UUID] = so.mapped_column(sa.UUID(), primary_key=True, default=uuid.uuid4, nullable=False)
    created_at: so.Mapped[datetime] = so.mapped_column(sa.DateTime(timezone=True), server_default=func.now(), nullable=True)

    message: so.Mapped[str] = so.mapped_column(sa.String(), nullable=False)
    timestamp: so.Mapped[datetime] = so.mapped_column(sa.DateTime(timezone=True), nullable=False)

    log_group: so.Mapped[LogGroup] = so.relationship(back_populates='log_items', lazy='selectin')
    log_group_id = so.mapped_column(sa.ForeignKey('log_group.id'), nullable=False)

    log_level: so.Mapped[LogLevel] = so.relationship(back_populates='log_items', lazy='selectin')
    log_level_name = so.mapped_column(sa.ForeignKey('log_level.name'), nullable=False)
