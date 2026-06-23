from collections import defaultdict

from app.database.models import Lesson

from app.database.user_repository import (
    get_user,
)

from app.themes.default import THEME as default
from app.themes.luxury import THEME as luxury
from app.themes.clean_girl import THEME as clean_girl
from app.themes.brother import THEME as brother
from app.themes.it_style import THEME as it_style


THEMES = {
    "default": default,
    "lux": luxury,
    "clean": clean_girl,
    "brat": brother,
    "it": it_style,
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


def format_session_schedule(
    lessons: list[Lesson],
    telegram_id=None,
) -> str:

    if not lessons:
        return "😄 Сессия не найдена"

    theme = get_theme(
        telegram_id
    )

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

    text = ""

    for (
        day,
        date,
    ), day_lessons in grouped.items():

        text += (
            "━━━━━━━━━━━━\n"
            f"🎓 {day} ({date})\n"
            "━━━━━━━━━━━━\n\n"
            f"📝 Экзаменов: "
            f"{len(day_lessons)}\n\n"
        )

        for lesson in day_lessons:

            text += (
                "➖➖➖➖➖➖➖➖➖\n"
                f"🎯 №{lesson.lesson_number} пара — "
                f"{lesson.lesson_time}\n\n"
            )

            text += (
                f"{theme['subject']} "
                f"<b>{lesson.subject}</b>\n"
            )

            if lesson.teacher:

                text += (
                    f"👨‍🏫 "
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

            else:

                text += (
                    "❓ Аудитория пока не указана\n"
                )

            if lesson.is_online:

                text += (
                    f"{theme['online']}"
                )

            text += "\n"

        text += "\n"

    return text
