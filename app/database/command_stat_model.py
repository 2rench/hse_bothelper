from sqlalchemy import (
    Column,
    Integer,
    String,
)

from app.database.database import Base


class CommandStat(Base):

    __tablename__ = "command_stats"

    id = Column(
        Integer,
        primary_key=True
    )

    command_name = Column(
        String,
        unique=True
    )

    count = Column(
        Integer,
        default=0
    )
