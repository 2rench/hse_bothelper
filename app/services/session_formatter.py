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


def _get_theme_from_user(
    user,
):

    if not user:
        return default

    return THEMES.get(
        user.get(
            "theme",
            "default",
        ),
        default,
    )


def emoji(
    lesson_count,
    lesson_type=None,
    theme_name=None,
):

    if theme_name == "default" and lesson_type:

        normalized_type = lesson_type.strip().lower()

        if normalized_type == "семинар":
            return "😵"

        if normalized_type == "лекция":
            return "😴"

    if lesson_count == 1:
        return "😋"

    if lesson_count in [2, 3]:
        return "😐"

    return "😵‍💫"


def _emoji_for_lessons(
    lessons,
    theme_name,
):

    lesson_type = None

    if theme_name == "default" and lessons:

        lesson_type = lessons[0].lesson_type

    return emoji(
        len(lessons),
        lesson_type=lesson_type,
        theme_name=theme_name,
    )


def _format_day_lessons(
    lessons,
    theme,
):

    blocks = []

    for lesson in lessons:

        text = (
            f"{theme['lesson']} "
            f"<b>№{lesson.lesson_number}</b> "
            f"<b><i>{lesson.lesson_time}</i></b>"
        )

        if lesson.room:

            text += (
                f", <b>{lesson.room}"
            )

            if lesson.building:

                text += (
                    f" [{lesson.building}]"
                )

            text += "</b>"

        text += "\n"

        text += (
            f"{lesson.subject}\n"
        )

        lesson_lines = []

        if lesson.teacher:

            lesson_lines.append(
                f"<i>{lesson.teacher}</i>"
            )

        check_subject = (
            lesson.subject.lower()
        )

        if (
            lesson.lesson_type
            and check_subject not in (
                "майнор",
                "военная кафедра",
            )
        ):

            lesson_lines.append(
                f"<b>{lesson.lesson_type.lower()}</b> "
                f"{theme['type']}"
            )

        if lesson_lines:

            text += (
                " ".join(
                    lesson_lines
                )
                + "\n"
            )

        if lesson.is_online:

            text += (
                f"{theme['online']}\n"
            )

        blocks.append(
            text.rstrip()
        )

    return "\n\n".join(
        blocks
    )


def format_session_schedule(
    lessons: list[Lesson],
    telegram_id=None,
) -> list[str]:
    """
    Возвращает список сообщений — по одному на каждый день сессии.
    Структура каждого сообщения повторяет основной форматер.
    """

    if not lessons:

        theme = get_theme(
            telegram_id
        )

        return [theme["no_lessons"]]

    user = None

    if telegram_id:

        user = get_user(
            telegram_id
        )

    theme = _get_theme_from_user(
        user
    )

    theme_name = "default"

    if user:

        theme_name = user.get(
            "theme",
            "default",
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

    messages = []

    for (
        day,
        date,
    ), day_lessons in grouped.items():

        text = (
            f"<b>{day} — {date}</b>\n\n"
        )

        text += (
            f"{_emoji_for_lessons(day_lessons, theme_name)} "
            f"{theme['pairs']}: "
            f"{len(day_lessons)}\n\n"
        )

        text += _format_day_lessons(
            day_lessons,
            theme,
        )

        messages.append(
            text.rstrip()
        )

    return messages
