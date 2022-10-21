from datetime import datetime
from uuid import uuid4

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    BigInteger,
    ForeignKey,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import  UUID
from .database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(
        UUID(as_uuid=True), primary_key=True, index=True, default=uuid4
    )
    name = Column(Text, nullable=True)
    mobile = Column(BigInteger, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(
        DateTime(timezone=True), nullable=False, default=datetime.utcnow
    )
    last_updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        onupdate=datetime.utcnow,
        default=datetime.utcnow,
    )
    last_updated_by = Column(UUID(as_uuid=True), nullable=True)

    __table_args__ = (
        UniqueConstraint(
            "mobile", name="unique_ids_user_mobile"
        ),
    )


class Group(Base):
    __tablename__ = "group"

    id = Column(
        UUID(as_uuid=True), primary_key=True, index=True, default=uuid4
    )
    name = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(
        DateTime(timezone=True), nullable=False, default=datetime.utcnow
    )
    created_by = Column(UUID(as_uuid=True), nullable=True)

    last_updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        onupdate=datetime.utcnow,
        default=datetime.utcnow,
    )
    last_updated_by = Column(UUID(as_uuid=True), nullable=True)


class Expense(Base):
    __tablename__ = "expense"

    id = Column(
        UUID(as_uuid=True), index=True, nullable=False, primary_key=True
    )
    title = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    total_amount = Column(Float, default=0.0)
    paid_by = Column(UUID(as_uuid=True), index=True, nullable=False)
    group_id = Column(
        UUID(as_uuid=True),
        ForeignKey("group.id"),
        index=True,
        nullable=False,
    )
    created_at = Column(
        DateTime(timezone=True), nullable=False, default=datetime.utcnow
    )
    created_by = Column(UUID(as_uuid=True), nullable=True)

    last_updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        onupdate=datetime.utcnow,
        default=datetime.utcnow,
    )
    last_updated_by = Column(UUID(as_uuid=True), nullable=True)


class UserGroupMapping(Base):
    __tablename__ = "user_group_mapping"

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("user.id"),
        index=True,
        nullable=False,
        primary_key=True
    )

    group_id = Column(
        UUID(as_uuid=True),
        ForeignKey("group.id"),
        index=True,
        nullable=False,
        primary_key=True 
    )
    # Explanation: user_id and group_id is a composite key (hence have to mention primary key in both)


class ExpenseUserMapping(Base):
    __tablename__ = "expense_user_mapping"

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("user.id"),
        index=True,
        nullable=False,
        primary_key=True
    )

    expense_id = Column(
        UUID(as_uuid=True),
        ForeignKey("expense.id"),
        index=True,
        nullable=False,
        primary_key=True
    )

    amount = Column(Float, default=0.0)