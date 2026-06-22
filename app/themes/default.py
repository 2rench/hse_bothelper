def no_lessons():
    return "На чиле, без пар 🤩"

def lessons_count(count):
    return f"😋 Пар: {count}"

def lesson_header(lesson):
    return (
        f"➖➖➖➖➖➖➖➖\n"
        f"☄️ <b>№{lesson.lesson_number} пара</b> — "
        f"<b>{lesson.lesson_time}</b>\n\n"
    )

def subject(lesson):
    return f"🎾 {lesson.subject}\n\n"

def lesson_type(lesson):
    return f"😴 <b>{lesson.lesson_type}</b>\n"

def teacher(lesson):
    return f"<b><i>{lesson.teacher}</i></b>\n\n"

def room(lesson):
    return f"🏫 {lesson.room} в {lesson.building} корпусе\n"

def online():
    return "🌐 Онлайн\n"
