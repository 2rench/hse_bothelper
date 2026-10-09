from datetime import datetime

from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.database.models import Lesson


def get_today_teachers() -> list[str]:
    today = datetime.now().strftime("%d.%m.%Y")

    db: Session = SessionLocal()

    try:
        teachers = (
            db.query(Lesson.teacher)
            .filter(
                Lesson.date == today,
                Lesson.teacher.isnot(None),
                Lesson.teacher != "",
            )
            .distinct()
            .order_by(Lesson.teacher)
            .all()
        )

        return [teacher[0] for teacher in teachers]

    finally:
        db.close()


def get_teacher_lessons_today(teacher: str) -> list[Lesson]:
    today = datetime.now().strftime("%d.%m.%Y")

    db: Session = SessionLocal()

    try:
        return (
            db.query(Lesson)
            .filter(
                Lesson.date == today,
                Lesson.teacher == teacher,
            )
            .order_by(
                Lesson.lesson_time,
                Lesson.lesson_number,
            )
            .all()
        )

    finally:
        db.close()
