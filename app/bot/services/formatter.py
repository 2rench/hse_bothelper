from collections import defaultdict

from app.services.session_formatter import (
    format_session_schedule,
)

from app.database.user_repository import (
    get_user,
)

from app.themes import (
    default,
    luxury,
    clean_girl,
    brother,
    it_style,
    # english,
    # chinese,
    # french,
)

THEMES = {
    "default": default,
    "lux": luxury,
    "clean": clean_girl,
    "brat": brother,
    "it": it_style,
    # "en": english,
    # "cn": chinese,
    # "fr": french,
}


def get_theme(
    telegram_id=None,
):

    if not telegram_id:
        return default

    user = get_user(
        telegram_id
    )

    if not user:
        return default

    return THEMES.get(
        user["theme"],
        default,
    )


def emoji(
    lesson_count,
):

    if lesson_count == 1:
        return "😋"

    if lesson_count in [2, 3]:
        return "😐"

    return "😵‍💫"


def format_lessons(
    lessons,
    telegram_id=None,
    title=None,
    group_by_day=False,
):

    theme = get_theme(
        telegram_id
    )

    if not lessons:

        return theme.no_lessons()

    if lessons[0].schedule_type == "session":

        return format_session_schedule(
            lessons
        )

    text = ""

    if title:

        text += (
            f"{title}\n\n"
        )

    if group_by_day:

        grouped = defaultdict(list)

        for lesson in lessons:

            grouped[
                (
                    lesson.day,
                    lesson.date,
                )
            ].append(
                lesson
            )

        for (
            day,
            date,
        ), day_lessons in grouped.items():

            text += (
                "━━━━━━━━━━━━\n"
                f"📅 {day} — {date}\n"
                "━━━━━━━━━━━━\n"
            )

            text += (
                theme.lessons_count(
                    len(day_lessons)
                )
            )

            text += "\n\n"

            text += _format_day_lessons(
                day_lessons,
                theme,
            )

            text += "\n"

        return text

    text += (
        theme.lessons_count(
            len(lessons)
        )
    )

    text += "\n\n"

    text += _format_day_lessons(
        lessons,
        theme,
    )

    return text


def _format_day_lessons(
    lessons,
    theme,
):

    text = ""

    for lesson in lessons:

        text += theme.lesson_header(
            lesson
        )

        text += theme.subject(
            lesson
        )

        text += theme.lesson_type(
            lesson
        )

        if lesson.teacher:

            text += theme.teacher(
                lesson
            )

        if lesson.room:

            text += theme.room(
                lesson
            ).rstrip()

            if lesson.building:

                text += (
                    f" в {lesson.building} корпусе"
                )

            text += "\n"

        if lesson.is_online:

            text += theme.online()

        text += "\n"

    return text
