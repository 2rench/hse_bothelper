from collections import defaultdict

from app.services.session_formatter import (
    format_session_schedule,
)

from app.database.user_repository import (
    get_user,
)

from app.themes.default import THEME as base_theme
from app.themes.niche_girl import THEME as girls_niche
from app.themes.luxury import THEME as girls_lux
from app.themes.clean_girl import THEME as girls_clean
from app.themes.brother import THEME as boys_brat
from app.themes.it_style import THEME as boys_it
# from app.themes.english import THEME as english
# from app.themes.chinese import THEME as chinese
# from app.themes.french import THEME as french


THEMES = {
    "base": base_theme,
    "girls_niche": girls_niche,
    "girls_lux": girls_lux,
    "girls_clean": girls_clean,
    "boys_brat": boys_brat,
    "boys_it": boys_it,
    # "english": english,
    # "chinese": chinese,
    # "french": french,
}


def emoji(lesson_count):

    if lesson_count == 1:
        return "😋"

    elif lesson_count in [2, 3]:
        return "😐"

    return "😵‍💫"


def format_lessons(
    lessons,
    telegram_id=None,
    title=None,
    group_by_day=False,
):

    if not lessons:
        return "На чиле, без пар 🤩"

    if lessons[0].schedule_type == "session":
        return format_session_schedule(
            lessons
        )

    theme = THEMES["base"]

    if telegram_id:

        user = get_user(
            telegram_id
        )

        if user:
            theme_name = user["theme"]

            theme = THEMES.get(
                theme_name,
                base_theme
            )

    text = ""

    if title:
        text += f"{title}\n\n"

    if group_by_day:

        grouped = defaultdict(list)

        for lesson in lessons:

            grouped[
                (lesson.day, lesson.date)
            ].append(lesson)

        for (
            day,
            date
        ), day_lessons in grouped.items():

            text += (
                "━━━━━━━━━━━━\n"
                f"{theme['day']} {day} — {date}\n"
                "━━━━━━━━━━━━\n"
                f"{emoji(len(day_lessons))} "
                f"{theme['pairs']}: {len(day_lessons)}\n\n"
            )

            text += _format_day_lessons(
                day_lessons,
                theme,
            )

            text += "\n"

        return text

    text += (
        f"{emoji(len(lessons))} "
        f"{theme['pairs']}: {len(lessons)}\n\n"
    )

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
            f"<b>№{lesson.lesson_number}</b> — "
            f"<b>{lesson.lesson_time}</b>\n\n"
        )

        text += (
            f"{theme['subject']} "
            f"{lesson.subject}\n\n"
        )

        text += (
            f"{theme['type']} "
            f"<b>{lesson.lesson_type}</b>\n"
        )

        if lesson.teacher:

            text += (
                f"<b><i>"
                f"{lesson.teacher}"
                f"</i></b>\n\n"
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
