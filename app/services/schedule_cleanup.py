import re

from sqlalchemy.orm import Session

from app.database.models import Lesson


def delete_schedule(
    db: Session,
    schedule_name: str,
) -> int:

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
