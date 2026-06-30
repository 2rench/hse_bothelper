from datetime import (
    datetime,
    UTC,
)

from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Boolean,
    DateTime,
)

from app.database.database import Base


class User(Base):

    __tablename__ = "users"

    id = Column(
        BigInteger,
        primary_key=True,
    )

    telegram_id = Column(
        BigInteger,
        unique=True,
        nullable=False,
    )

    group_name = Column(
        String,
        nullable=False,
    )

    schedule_updates = Column(
        Boolean,
        default=True,
        nullable=False,
    )

    tomorrow_notifications = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    theme = Column(
        String,
        default="default",
        nullable=False,
    )

    created_date = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )
