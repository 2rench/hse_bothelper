from collections import defaultdict

from app.database.models import Lesson


def format_session_schedule(
    lessons: list[Lesson],
) -> str:

    if not lessons:
        return "Сессия не найдена 😄"

    grouped = defaultdict(list)

    for lesson in lessons:
        grouped[
            (lesson.day, lesson.date)
        ].append(lesson)

    # session_name = lessons[0].schedule_name

    # text = f"🎓 <b>{session_name}</b>\n\n"
    text = ""
    for (day, date), day_lessons in grouped.items():

        text += (
            "━━━━━━━━━━━━\n"
            f"📅 {day} ({date})\n"
            "━━━━━━━━━━━━\n\n"
        )

        for lesson in day_lessons:

            text += (
                f"☄️ <b>№{lesson.lesson_number} пара — "
                f"{lesson.lesson_time}</b>\n\n"
            )

            text += f"🥶 <b>{lesson.subject}</b>\n\n"

            if lesson.teacher:
                text += (
                    f"<b><i>{lesson.teacher}</i></b>\n"
                )

            if lesson.room:

                text += f"💥 Аудитория: {lesson.room}"

                if lesson.building:
                    text += (
                        f" в {lesson.building} корпусе"
                    )

                text += "\n"

            else:

                text += (
                    "🫤 Информации по аудитории нет\n"
                )

            if lesson.is_online:
                text += "🌐 Онлайн\n"

            text += "\n"

    return text
