from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.database.database import Base


class Lesson(Base):

    __tablename__ = "lessons"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    group: Mapped[str] = mapped_column(String)

    day: Mapped[str] = mapped_column(String)

    date: Mapped[str] = mapped_column(String)

    lesson_number: Mapped[str] = mapped_column(String)

    lesson_time: Mapped[str] = mapped_column(String)

    subject: Mapped[str | None] = mapped_column(
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

    raw_text: Mapped[str] = mapped_column(String)

    sheet: Mapped[str] = mapped_column(String)