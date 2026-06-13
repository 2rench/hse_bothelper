from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.database.database import Base


class ScheduleFile(Base):

    __tablename__ = "schedule_files"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    file_name: Mapped[str] = mapped_column(
        String,
    )

    file_url: Mapped[str] = mapped_column(
        String,
        unique=True,
    )

    file_hash: Mapped[str] = mapped_column(
        String,
    )
