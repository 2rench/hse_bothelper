from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.database.database import Base


class ScheduleVersion(Base):

    __tablename__ = "schedule_versions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    schedule_name: Mapped[str] = mapped_column(
        String,
    )

    file_hash: Mapped[str] = mapped_column(
        String,
    )
