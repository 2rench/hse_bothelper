import re

from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.database.models import Lesson
from datetime import datetime, timedelta
from sqlalchemy import not_


def get_lessons_by_date(
    group: str,
    date: str,
) -> list[Lesson]:

    db: Session = SessionLocal()

    changes = (
        db.query(Lesson)
        .filter(
            Lesson.group_name == group,
            Lesson.date == date,
            Lesson.schedule_type == "changes",
        )
        .order_by(
            Lesson.lesson_number
        )
        .all()
    )

    if changes:

        db.close()

        return changes

    base = (
        db.query(Lesson)
        .filter(
            Lesson.group_name == group,
            Lesson.date == date,
            Lesson.schedule_type == "base",
        )
        .order_by(
            Lesson.lesson_number
        )
        .all()
    )

    db.close()

    return base



def get_week_lessons(
    group: str,
) -> list[Lesson]:

    db: Session = SessionLocal()

    lessons = (
        db.query(Lesson)
        .filter(
            Lesson.group_name == group,

            Lesson.schedule_type.in_(
                ["changes", "base"]
            )
        )
        .all()
    )

    db.close()

    if not lessons:
        return []

    today = datetime.now()

    week_start = today - timedelta(
        days=today.weekday()
    )

    week_start = week_start.replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )

    week_end = week_start + timedelta(
        days=6
    )

    grouped = {}

    for lesson in lessons:

        lesson_date = datetime.strptime(
            lesson.date,
            "%d.%m.%Y"
        )

        if not (
            week_start
            <= lesson_date
            <= week_end
        ):
            continue

        grouped.setdefault(
            lesson.date,
            []
        ).append(
            lesson
        )

    result = []

    for date, day_lessons in grouped.items():

        changes = [
            l for l in day_lessons
            if l.schedule_type == "changes"
        ]

        if changes:

            result.extend(
                changes
            )

        else:

            result.extend(
                [
                    l for l in day_lessons
                    if l.schedule_type == "base"
                ]
            )

    result.sort(
        key=lambda x: (
            datetime.strptime(
                x.date,
                "%d.%m.%Y"
            ),
            int(x.lesson_number),
        )
    )

    return result


def get_tomorrow_study_date(
    group: str,
) -> str | None:

    current = get_current_study_date(
        group
    )

    if current is None:
        return None

    current_date = datetime.strptime(
        current,
        "%d.%m.%Y"
    )

    tomorrow = (
        current_date
        + timedelta(days=1)
    )

    return tomorrow.strftime(
        "%d.%m.%Y"
    )

def get_current_study_date(
    group: str,
) -> str | None:

    db: Session = SessionLocal()

    lessons = (
        db.query(Lesson)
        .filter(
            Lesson.group_name == group,

            not_(
                Lesson.schedule_name.like(
                    "СЕССИЯ%"
                )
            ),
        )
        .all()
    )

    db.close()

    if not lessons:
        return None

    today = datetime.now()

    parsed_dates = []

    for lesson in lessons:

        try:

            lesson_date = datetime.strptime(
                lesson.date,
                "%d.%m.%Y"
            )

            parsed_dates.append(
                lesson_date
            )

        except:
            continue

    if not parsed_dates:
        return None

    parsed_dates.sort()

    for date in parsed_dates:

        if date >= today.replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
        ):

            return date.strftime(
                "%d.%m.%Y"
            )

    return parsed_dates[-1].strftime(
        "%d.%m.%Y"
    )


def get_week_lessons_by_number(
    group: str,
    week: int,
):

    db: Session = SessionLocal()

    lessons = (
        db.query(Lesson)
        .filter(
            Lesson.group_name == group,

            Lesson.schedule_name.like(
                f"%неделя №{week}%"
            ),

            not_(
                Lesson.schedule_name.like(
                    "СЕССИЯ%"
                )
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
