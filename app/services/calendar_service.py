import hashlib
import re

from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.database.models import Lesson


PERM_TZ = ZoneInfo(
    "Asia/Yekaterinburg"
)


TIME_PATTERN = re.compile(
    r"(\d{1,2}):(\d{2})\s*[-–—]\s*(\d{1,2}):(\d{2})"
)


def _escape_ical(
    value: str,
) -> str:

    value = str(
        value or ""
    )

    value = value.replace(
        "\\",
        "\\\\",
    )

    value = value.replace(
        ";",
        "\\;",
    )

    value = value.replace(
        ",",
        "\\,",
    )

    value = value.replace(
        "\r\n",
        "\\n",
    )

    value = value.replace(
        "\n",
        "\\n",
    )

    return value


def _parse_lesson_datetime(
    date_str: str,
    time_str: str,
):

    match = TIME_PATTERN.search(
        time_str or ""
    )

    if not match:
        return None, None

    start_hour = int(
        match.group(1)
    )

    start_minute = int(
        match.group(2)
    )

    end_hour = int(
        match.group(3)
    )

    end_minute = int(
        match.group(4)
    )

    try:

        date = datetime.strptime(
            date_str,
            "%d.%m.%Y",
        )

    except ValueError:

        return None, None

    start = datetime(
        date.year,
        date.month,
        date.day,
        start_hour,
        start_minute,
        tzinfo=PERM_TZ,
    )

    end = datetime(
        date.year,
        date.month,
        date.day,
        end_hour,
        end_minute,
        tzinfo=PERM_TZ,
    )

    return start, end


def _format_ical_datetime(
    value: datetime,
) -> str:

    return (
        value
        .astimezone(timezone.utc)
        .strftime(
            "%Y%m%dT%H%M%SZ"
        )
    )


def _get_effective_lessons(
    group: str,
) -> list[Lesson]:

    db: Session = SessionLocal()

    try:

        lessons = (
            db.query(Lesson)
            .filter(
                Lesson.group_name == group,
                Lesson.schedule_type.in_(
                    [
                        "base",
                        "changes",
                    ]
                ),
            )
            .all()
        )

        if not lessons:
            return []

        today = datetime.now(
            PERM_TZ
        ).replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
        )

        start_date = (
            today
            - timedelta(days=30)
        )

        end_date = (
            today
            + timedelta(days=180)
        )

        grouped = {}

        for lesson in lessons:

            if not lesson.date:
                continue

            try:

                lesson_date = datetime.strptime(
                    lesson.date,
                    "%d.%m.%Y",
                )

            except ValueError:

                continue

            if (
                lesson_date < start_date.replace(
                    tzinfo=None
                )
                or
                lesson_date > end_date.replace(
                    tzinfo=None
                )
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
                lesson
                for lesson in day_lessons
                if lesson.schedule_type
                == "changes"
            ]

            if changes:

                result.extend(
                    changes
                )

            else:

                result.extend(
                    [
                        lesson
                        for lesson in day_lessons
                        if lesson.schedule_type
                        == "base"
                    ]
                )

        result.sort(
            key=lambda lesson: (
                datetime.strptime(
                    lesson.date,
                    "%d.%m.%Y",
                ),
                str(
                    lesson.lesson_number
                ),
                str(
                    lesson.lesson_time
                ),
            )
        )

        return result

    finally:

        db.close()


def build_calendar(
    group: str,
    excluded_subjects: list[str] | None = None,
) -> str:

    lessons = _get_effective_lessons(
        group
    )

    excluded = set(
        excluded_subjects or []
    )

    now = datetime.now(
        timezone.utc
    )

    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//HSE Perm Schedule Bot//RU",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "X-WR-CALNAME:HSE Расписание",
    ]

    uid_counter = {}

    for lesson in lessons:

        if (
            lesson.subject
            and lesson.subject in excluded
        ):

            continue

        start, end = _parse_lesson_datetime(
            lesson.date,
            lesson.lesson_time,
        )

        if start is None or end is None:
            continue

        slot_key = (
            lesson.date,
            str(
                lesson.lesson_number
            ),
            str(
                lesson.lesson_time
            ),
        )

        uid_counter[
            slot_key
        ] = (
            uid_counter.get(
                slot_key,
                0,
            )
            + 1
        )

        ordinal = uid_counter[
            slot_key
        ]

        uid_source = (
            f"{group}|"
            f"{lesson.date}|"
            f"{lesson.lesson_number}|"
            f"{lesson.lesson_time}|"
            f"{ordinal}"
        )

        uid = (
            hashlib.sha256(
                uid_source.encode(
                    "utf-8"
                )
            ).hexdigest()
            + "@hse-schedule-bot"
        )

        summary = (
            lesson.subject
            or "Пара"
        )

        description_parts = []

        if lesson.teacher:

            description_parts.append(
                f"Преподаватель: "
                f"{lesson.teacher}"
            )

        if lesson.lesson_type:

            description_parts.append(
                f"Тип: "
                f"{lesson.lesson_type}"
            )

        if lesson.is_online:

            description_parts.append(
                "Онлайн"
            )

        description = "\n".join(
            description_parts
        )

        location = ""

        if lesson.room:

            location = str(
                lesson.room
            )

            if lesson.building:

                location += (
                    f" [{lesson.building}]"
                )

        lines.extend(
            [
                "BEGIN:VEVENT",
                f"UID:{uid}",
                (
                    "DTSTAMP:"
                    f"{_format_ical_datetime(now)}"
                ),
                (
                    "DTSTART:"
                    f"{_format_ical_datetime(start)}"
                ),
                (
                    "DTEND:"
                    f"{_format_ical_datetime(end)}"
                ),
                (
                    "SUMMARY:"
                    f"{_escape_ical(summary)}"
                ),
                (
                    "DESCRIPTION:"
                    f"{_escape_ical(description)}"
                ),
                (
                    "LOCATION:"
                    f"{_escape_ical(location)}"
                ),
                "STATUS:CONFIRMED",
                "END:VEVENT",
            ]
        )

    lines.append(
        "END:VCALENDAR"
    )

    return (
        "\r\n".join(lines)
        + "\r\n"
    )
