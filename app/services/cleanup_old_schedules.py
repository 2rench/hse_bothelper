import re

from app.database.database import SessionLocal
from app.database.models import Lesson


def cleanup_old_schedules(
    current_week: int,
):

    db = SessionLocal()

    keys = (
        db.query(
            Lesson.schedule_key
        )
        .distinct()
        .all()
    )

    for row in keys:

        key = row[0]

        if key is None:
            continue

        match = re.search(
            r"_(\d+)$",
            key
        )

        if not match:
            continue

        week = int(
            match.group(1)
        )

        if week < current_week:

            print(
                f"DELETE OLD {key}"
            )

            db.query(Lesson).filter(
                Lesson.schedule_key == key
            ).delete()

    db.commit()
    db.close()
