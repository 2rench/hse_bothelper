from collections import defaultdict

from app.database.models import Lesson


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
        text += f"📅 {day} ({date})\n\n"
        text += f"📚 Пар: {len(day_lessons)}\n\n"

        for lesson in day_lessons:
            text += f"{lesson.lesson_number} {lesson.lesson_time}\n"
            text += f"{lesson.subject}\n"
            text += f"{lesson.lesson_type}\n"

            if lesson.teacher:
                text += f"{lesson.teacher}\n"

            if lesson.room:
                text += f"Аудитория: {lesson.room}"
                if lesson.building:
                    text += f" [{lesson.building}]"
                text += "\n"

            if lesson.is_online:
                text += "🌐 Онлайн\n"

            text += "\n"

    return text
