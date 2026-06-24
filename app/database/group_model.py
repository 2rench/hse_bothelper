from sqlalchemy import (
    Column,
    Integer,
    String,
)

from app.database.database import Base


class Group(Base):

    __tablename__ = "groups"

    id = Column(
        Integer,
        primary_key=True
    )

    education_year = Column(
        String
    )

    group_name = Column(
        String,
        unique=True
    )
