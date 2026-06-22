def no_lessons():
    return "Дорогая, сегодня можно отдыхать 🤍"

def lessons_count(count):
    return f"🎀 Сегодня пар: {count}"

def lesson_header(lesson):
    return (
        f"🩷 <b>{lesson.lesson_time}</b>\n"
    )

def subject(lesson):
    return f"📚 {lesson.subject}\n"

def lesson_type(lesson):
    return f"✨ {lesson.lesson_type}\n"

def teacher(lesson):
    return f"👩🏻‍🏫 {lesson.teacher}\n"

def room(lesson):
    return f"🏛 {lesson.room}, корпус {lesson.building}\n"

def online():
    return "💻 Онлайн\n"
