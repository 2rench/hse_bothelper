from collections import defaultdict

from app.services.session_formatter import (
    format_session_schedule,
)

from app.database.user_repository import (
    get_user,
)

from app.themes.default import THEME as default
from app.themes.luxury import THEME as luxury
from app.themes.clean_girl import THEME as clean_girl
from app.themes.brother import THEME as brother
from app.themes.it_style import THEME as it_style
from app.themes.english import THEME as english
from app.themes.chinese import THEME as chinese
from app.themes.french import THEME as french


THEMES = {
    "default": default,
    "lux": luxury,
    "clean": clean_girl,
    "brat": brother,
    "it": it_style,
    "english": english,
    "french": french,
    "chinese": chinese,
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
        return theme["no_lessons"]

    if lessons[0].schedule_type == "session":

        return format_session_schedule(
            lessons,
            telegram_id,
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
                f"{theme['day']} {day} — {date}\n"
                "━━━━━━━━━━━━\n"
            )

            text += (
                f"{emoji(len(day_lessons))} "
                f"{theme['pairs']}: "
                f"{len(day_lessons)}"
            )

            text += "\n\n"

            text += _format_day_lessons(
                day_lessons,
                theme,
            )

            text += "\n"

        return text

    text += (
        f"{emoji(len(lessons))} "
        f"{theme['pairs']}: "
        f"{len(lessons)}"
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

        text += (
            "➖➖➖➖➖➖➖➖\n"
            f"{theme['lesson']} "
            f"<b>№{lesson.lesson_number} пара</b> — "
            f"<b>{lesson.lesson_time}</b>\n\n"
        )

        text += (
            f"{theme['subject']} "
            f"{lesson.subject}\n\n"
        )

        if lesson.lesson_type:

            text += (
                f"{theme['type']} "
                f"<b>{lesson.lesson_type}</b>\n"
            )

        if lesson.teacher:

            text += (
                f"<b><i>{lesson.teacher}</i></b>\n\n"
            )

        if lesson.room:

            text += (
                f"{theme['room']} "
                f"{lesson.room}"
            )

            if lesson.building:

                text += (
                    f" в {lesson.building} корпусе"
                )

            text += "\n"

        if lesson.is_online:

            text += (
                f"{theme['online']}\n"
            )

        text += "\n"

    return text

def get_today_no_lessons(
    telegram_id=None,
):
    return get_theme(
        telegram_id
    )["today_no_lessons"]


def get_tomorrow_no_lessons(
    telegram_id=None,
):
    return get_theme(
        telegram_id
    )["tomorrow_no_lessons"]


def get_week_no_lessons(
    telegram_id=None,
):
    return get_theme(
        telegram_id
    )["week_no_lessons"]

