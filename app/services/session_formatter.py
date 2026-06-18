from collections import defaultdict

from app.database.models import Lesson

from app.bot.services.formatter import get_lesson_status

def format_session_schedule(
    lessons: list[Lesson],
) -> str:

    if not lessons:
        return "Сессия не найдена 😄"

    grouped = defaultdict(list)

    for lesson in lessons:
        key = (
            lesson.day,
            lesson.date,
        )
        grouped[key].append(lesson)

    # Получаем название сессии из первого урока
    session_name = lessons[0].schedule_name if lessons else ""

    text = f"🎓 {session_name}\n\n"

    for (day, date), day_lessons in grouped.items():
        text += f"━━━━━━━━━━━━\n"
        text += f"📅 {day} ({date})\n"
        text += f"━━━━━━━━━━━━\n\n"

        for lesson in day_lessons:
            text += f"""{get_lesson_status(lesson)} <b>№{lesson.lesson_number}
            пара — {lesson.lesson_time}</b>\n"""
            text += f"🥶 {lesson.subject}\n"

            if lesson.teacher:
                text += f"<b><i>{lesson.teacher}</i></b>\n"

            if lesson.room:
                text += f"💥 Аудитория: {lesson.room}"
                if lesson.building:
                    text += f"🏫 Корпус: {lesson.building}"
                text += "\n"

            if lesson.is_online:
                text += "🌐 Онлайн\n"

            text += "\n"

    return text
