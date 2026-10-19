from collections import defaultdict

from app.database.models import Lesson
from app.database.user_repository import get_user

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
    "luxury": luxury,
    "clean_girl": clean_girl,
    "brother": brother,
    "it_style": it_style,
    "english": english,
    "french": french,
    "chinese": chinese,
}


MILITARY_SUBJECTS = (
    "военная кафедра",
    "военная кафедра (военный учебный центр)",
)


def get_theme(telegram_id=None):
    if not telegram_id:
        return default

    user = get_user(telegram_id)

    if not user:
        return default

    return THEMES.get(
        user["theme"],
        default,
    )


def _get_theme_from_user(user):
    if not user:
        return default

    return THEMES.get(
        user.get("theme", "default"),
        default,
    )


def _format_day_lessons(lessons, theme):
    blocks = []

    for lesson in lessons:
        text = (
            f"{theme['lesson']} "
            f"<b>№{lesson.lesson_number}</b> "
            f"<b><i>{lesson.lesson_time}</i></b>"
        )

        if lesson.room:
            text += f", <b>{lesson.room}"

            if lesson.building:
                text += f" [{lesson.building}]"

            text += "</b>"

        text += "\n"
        text += f"{lesson.subject}\n"

        if lesson.teacher:
            text += f"<i>{lesson.teacher}</i>\n"

        if lesson.is_online:
            text += f"{theme['online']}\n"

        blocks.append(text.rstrip())

    return "\n\n".join(blocks)


def _filter_military_department(lessons):
    return [
        lesson
        for lesson in lessons
        if lesson.subject.strip().lower()
        not in MILITARY_SUBJECTS
    ]


def format_session_schedule(
    lessons: list[Lesson],
    telegram_id=None,
    week=None,
) -> list[str]:

    if not lessons:
        theme = get_theme(telegram_id)
        return [theme["no_lessons"]]

    lessons = _filter_military_department(lessons)

    if not lessons:
        theme = get_theme(telegram_id)
        return [theme["no_lessons"]]

    user = get_user(telegram_id) if telegram_id else None

    theme = _get_theme_from_user(user)

    grouped = defaultdict(list)

    for lesson in lessons:
        grouped[
            (lesson.day, lesson.date)
        ].append(lesson)

    messages = []

    for (day, date), day_lessons in grouped.items():
        text = f"<b>{day} — {date}</b>\n\n"

        text += _format_day_lessons(
            day_lessons,
            theme,
        )

        messages.append(text.rstrip())

    if messages and week is not None:
        messages[0] = (
            f"🎓 Сессия (неделя №{week})\n\n"
            f"{messages[0]}"
        )

    return messages


def format_session_schedule_joined(
    lessons: list[Lesson],
    telegram_id=None,
) -> str:
    return "\n\n".join(
        format_session_schedule(
            lessons,
            telegram_id,
        )
    )
