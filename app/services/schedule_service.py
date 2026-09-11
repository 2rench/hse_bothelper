import re

from datetime import datetime, timedelta

from sqlalchemy import not_
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.database.models import Lesson


def get_lessons_by_date(
    group: str,
    date: str,
) -> list[Lesson]:

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

    lessons = list(
        unique.values()
    )

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


def get_week_lessons_by_number(
    group: str,
    week: int,
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

    pattern = re.compile(
        r"недел(?:я|и)\s*№?\s*(\d+)",
        re.IGNORECASE,
    )

    result = []

    for lesson in lessons:

        schedule_name = (
            lesson.schedule_name
            or ""
        )

        match = pattern.search(
            schedule_name
        )

        if not match:
            continue

        schedule_week = int(
            match.group(1)
        )

        if schedule_week == week:

            result.append(
                lesson
            )

    unique = {}

    for lesson in result:

        key = (
            lesson.date,
            lesson.lesson_number,
            lesson.subject,
            lesson.teacher,
            lesson.room,
            lesson.building,
        )

        unique[key] = lesson

    result = list(
        unique.values()
    )

    result.sort(
        key=lambda x: (
            datetime.strptime(
                x.date,
                "%d.%m.%Y"
            ),
            int(x.lesson_number)
            if str(x.lesson_number).isdigit()
            else 0,
        )
    )

    return result


def get_available_week_numbers(
    group: str,
) -> list[int]:

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

    pattern = re.compile(
        r"недел(?:я|и)\s*№?\s*(\d+)",
        re.IGNORECASE,
    )

    weeks = set()

    for lesson in lessons:

        schedule_name = (
            lesson.schedule_name
            or ""
        )

        match = pattern.search(
            schedule_name
        )

        if not match:
            continue

        weeks.add(
            int(
                match.group(1)
            )
        )

    return sorted(
        weeks
    )


def get_current_schedule_week(
    group: str,
) -> int | None:

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

    pattern = re.compile(
        r"недел(?:я|и)\s*№?\s*(\d+)",
        re.IGNORECASE,
    )

    today = datetime.now().replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )

    week_dates = {}

    for lesson in lessons:

        try:

            lesson_date = datetime.strptime(
                lesson.date,
                "%d.%m.%Y"
            )

        except Exception:

            continue

        schedule_name = (
            lesson.schedule_name
            or ""
        )

        match = pattern.search(
            schedule_name
        )

        if not match:
            continue

        week = int(
            match.group(1)
        )

        week_dates.setdefault(
            week,
            []
        ).append(
            lesson_date
        )

    if not week_dates:
        return None

    for week, dates in week_dates.items():

        week_start = min(dates)
        week_end = max(dates)

        if (
            week_start
            <= today
            <= week_end
        ):

            return week

    future_weeks = []

    for week, dates in week_dates.items():

        week_start = min(dates)

        if week_start > today:

            future_weeks.append(
                (
                    week_start,
                    week,
                )
            )

    if future_weeks:

        future_weeks.sort()

        return future_weeks[0][1]

    return max(
        week_dates
    )


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

        except Exception:

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


def get_week_subjects(
    group: str,
) -> list[str]:

    lessons = get_week_lessons(
        group
    )

    subjects = {
        lesson.subject.strip()
        for lesson in lessons
        if lesson.subject
        and lesson.subject.strip()
    }

    return sorted(
        subjects,
        key=lambda subject: subject.lower(),
    )
