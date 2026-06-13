import re

from app.database.database import (
    SessionLocal,
)

from app.database.models import (
    Lesson,
)


def get_all_sessions():

    db = SessionLocal()

    sessions = (
        db.query(
            Lesson.schedule_name
        )
        .filter(
            Lesson.schedule_name.like(
                "СЕССИЯ%"
            )
        )
        .distinct()
        .all()
    )

    db.close()

    result = [
        row[0]
        for row in sessions
    ]

    def get_week_number(name):

        match = re.search(
            r"неделя №(\d+)",
            name,
        )

        if match:
            return int(
                match.group(1)
            )

        return 999

    result.sort(
        key=get_week_number
    )

    return result
