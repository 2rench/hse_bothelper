import re

from app.database.database import (
    SessionLocal,
)

from app.database.models import (
    Lesson,
)

from datetime import datetime

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

    latest = {}

    for row in sessions:

        name = row[0]

        week = extract_week_number(
            name
        )

        if week not in latest:
            latest[week] = name
            continue

        if "изм." in name:
            latest[week] = name

    result = list(
        latest.values()
    )

    result.sort(
        key=extract_week_number
    )

    return result


def extract_week_number(
    session_name: str,
) -> int:

    match = re.search(
        r"неделя №(\d+)",
        session_name,
    )

    if not match:
        return 0

    return int(
        match.group(1)
    )

def get_session_lessons(
    group_name: str,
    schedule_name: str,
):

    db = SessionLocal()

    lessons = (
        db.query(Lesson)
        .filter(
            Lesson.group_name
            == group_name,

            Lesson.schedule_name
            == schedule_name,
        )
        .order_by(
            Lesson.date,
            Lesson.lesson_number,
        )
        .all()
    )

    db.close()

    return lessons


def get_session_by_week(
    group_name: str,
    week: int,
):

    db = SessionLocal()

    lessons = (
        db.query(Lesson)
        .filter(
            Lesson.group_name
            == group_name,

            Lesson.schedule_name.like(
                f"%неделя №{week}%"
            ),

            Lesson.schedule_name.like(
                "СЕССИЯ%"
            ),
        )
        .order_by(
            Lesson.date,
            Lesson.lesson_number,
        )
        .all()
    )

    db.close()

    return lessons
