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
    """
    Возвращает пары группы
    на конкретную дату.
    """

    db: Session = SessionLocal()

    lessons = (
        db.query(Lesson)
        .filter(
            Lesson.group_name == group,
            Lesson.date == date,

            not_(
                Lesson.schedule_name.like(
                    "СЕССИЯ%"
                )
            ),
        )
        .order_by(
            Lesson.lesson_number
        )
        .all()
    )

    db.close()

    return lessons


def get_week_lessons(
    group: str,
) -> list[Lesson]:

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
        return []

    unique = {}

    for lesson in lessons:

        key = (
            lesson.date,
            lesson.lesson_number,
            lesson.subject,
            lesson.teacher,
            lesson.room,
        )

        unique[key] = lesson

    lessons = list(unique.values())

    lessons.sort(
        key=lambda x: (
            datetime.strptime(
                x.date,
                "%d.%m.%Y"
            ),
            int(x.lesson_number),
        )
    )

    today = datetime.now()

    # ПОНЕДЕЛЬНИК текущей недели
    week_start = today - timedelta(
        days=today.weekday()
    )

    week_start = week_start.replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )

    # ВОСКРЕСЕНЬЕ
    week_end = week_start + timedelta(
        days=6
    )

    filtered = []

    for lesson in lessons:

        lesson_date = datetime.strptime(
            lesson.date,
            "%d.%m.%Y"
        )

        if (
            week_start
            <= lesson_date
            <= week_end
        ):

            filtered.append(
                lesson
            )

    return filtered

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
