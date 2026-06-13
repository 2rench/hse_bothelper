from collections import defaultdict


def format_lessons(
    lessons,
    title: str | None = None,
    group_by_day: bool = False,
):

    """
    Форматирует расписание
    в Telegram-текст.
    """

    if not lessons:

        return "Пар нет 😄"

    text = ""

    if title:

        text += f"{title}\n\n"

    # Для /week
    if group_by_day:

        grouped = defaultdict(list)

        for lesson in lessons:

            grouped[
                (lesson.day, lesson.date)
            ].append(lesson)

        for (
            day,
            date,
        ), day_lessons in grouped.items():

            text += (
                f"━━━━━━━━━━━━\n"
                f"📅 {day} ({date})\n"
                f"📚 Пар: {len(day_lessons)}\n\n"
            )

            text += _format_day_lessons(
                day_lessons
            )

            text += "\n"

        return text

    # Для /today
    text += (
        f"📚 Пар: {len(lessons)}\n\n"
    )

    text += _format_day_lessons(
        lessons
    )

    return text


def _format_day_lessons(lessons):

    """
    Форматирует пары
    одного дня.
    """

    text = ""

    for lesson in lessons:

        text += (
            f"<b>{lesson.lesson_number}</b> "
            f"{lesson.lesson_time}\n"
        )

        text += f"{lesson.subject}\n"
        text += f"{lesson.lesson_type}\n"

        if lesson.teacher:

            text += (
                f"{lesson.teacher}\n"
            )

        if lesson.room:

            text += (
                f"Аудитория: "
                f"{lesson.room}"
            )

            if lesson.building:

                text += (
                    f" [{lesson.building}]"
                )

            text += "\n"

        if lesson.is_online:

            text += (
                "🌐 Онлайн\n"
            )

        text += "\n"

    return text
