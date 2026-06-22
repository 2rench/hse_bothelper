from sqlalchemy import (
    String,
    Integer,
    Boolean,

)

from app.database.database import Base
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

class Lesson(Base):

    __tablename__ = "lessons"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    group_name: Mapped[str] = mapped_column(
        String,
    )

    day: Mapped[str] = mapped_column(
        String,
    )

    date: Mapped[str] = mapped_column(
        String,
    )

    lesson_number: Mapped[str] = mapped_column(
        String,
    )

    lesson_time: Mapped[str] = mapped_column(
        String,
    )

    subject: Mapped[str] = mapped_column(
        String,
    )

    schedule_name: Mapped[str] = mapped_column(
        String,
        nullable=True,
    )

    lesson_type: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    teacher: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    room: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    building: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    is_online: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    schedule_type: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    schedule_key: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

class CommandStat(Base):

    __tablename__ = "command_stats"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    command_name: Mapped[str] = mapped_column(
        String
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
    )
