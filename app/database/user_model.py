from sqlalchemy import Column
from sqlalchemy import Integer, BigInteger
from sqlalchemy import String
from sqlalchemy import Boolean

from app.database.database import Base


class User(Base):

    __tablename__ = "users"

    id = Column(
        BigInteger,
        primary_key=True
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
