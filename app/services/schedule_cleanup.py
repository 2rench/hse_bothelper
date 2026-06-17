import re

from sqlalchemy.orm import Session

from sqlalchemy import func

from app.database.models import Lesson


def delete_schedule(
    db: Session,
    schedule_name: str,
) -> int:

    schedule_name = schedule_name.lower()

    if "базовое" in schedule_name:

        return (
            db.query(Lesson)
            .filter(
                Lesson.schedule_type == "base"
            )
            .delete(
                synchronize_session=False
            )
        )

    if "сессия" in schedule_name:

        return (
            db.query(Lesson)
            .filter(
                Lesson.schedule_type == "session"
            )
            .delete(
                synchronize_session=False
            )
        )

    base_name = re.sub(
        r"\s+с изм\..*$",
        "",
        schedule_name,
        flags=re.IGNORECASE,
    )

    return (
        db.query(Lesson)
        .filter(
            Lesson.schedule_name.like(
                f"{base_name}%"
            )
        )
        .delete(
            synchronize_session=False
        )
    )
