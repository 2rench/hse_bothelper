def no_lessons():
    return "Зай, сегодня никаких пар ✨"

def lessons_count(count):
    return f"💎 Дел на сегодня: {count}"

def lesson_header(lesson):
    return (
        f"━━━━━━━━━━━━\n"
        f"⏰ {lesson.lesson_time}\n\n"
    )

def subject(lesson):
    return f"🥂 {lesson.subject}\n"

def lesson_type(lesson):
    return f"✨ {lesson.lesson_type}\n"

def teacher(lesson):
    return f"🎓 {lesson.teacher}\n"

def room(lesson):
    return f"🏛 {lesson.room}, {lesson.building} корпус\n"

def online():
    return "💻 Online\n"
