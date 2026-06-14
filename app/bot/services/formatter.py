from collections import defaultdict


def emoji(lesson_count):
    if lesson_count == 1:
        EMOJI_LESSONS_DAY = '😋'
    elif lesson_count > 1 and lesson_count <= 3:
        EMOJI_LESSONS_DAY = '😐'
    else:
        EMOJI_LESSONS_DAY = '😵‍💫'

    return EMOJI_LESSONS_DAY

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

        return "На чиле, без пар 🤩"

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
                f"📅 {day} — {date}\n"
                f"{emoji(len(lessons))} Пар: {len(day_lessons)}\n\n"
            )

            text += _format_day_lessons(
                day_lessons
            )

            text += "\n"

        return text

    # Для /today
    text += (
        f"{emoji(len(lessons))} Пар: {len(lessons)}\n\n"
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
            f"☄️<b>№{lesson.lesson_number} пара</b> — "
            f"{lesson.lesson_time}\n"
        )
        if lesson.lesson_type == 'Семинар':
            EMOJI_FOR_LESSON_TYPE = '🙄'
        else:
            EMOJI_FOR_LESSON_TYPE = '😴'

        text += f"🎾 Предмет: {lesson.subject}\n"
        text += f"{EMOJI_FOR_LESSON_TYPE} {lesson.lesson_type}\n"

        if lesson.teacher:

            text += (
                f"🙂 Преподаватель: {lesson.teacher}\n"
            )

        if lesson.room:

            text += (
                f"⭐ Аудитория: "
                f"{lesson.room} \n"
            )

            if lesson.building:

                text += (
                    f"🏫 Корпус: {lesson.building}"
                )

            text += "\n"

        if lesson.is_online:

            text += (
                "🌐 Онлайн\n"
            )

        text += "\n"

    return text
