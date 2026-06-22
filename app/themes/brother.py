def no_lessons():
    return "Брат сегодня чётенько аккуратненько без пар двигаемся 😎"

def lessons_count(count):
    return f"🤝 Сегодня на суете {count} раз"

def lesson_header(lesson):
    return (
        f"💀 {lesson.lesson_time}\n"
    )

def subject(lesson):
    return f"📖 {lesson.subject}\n"

def lesson_type(lesson):
    return f"⚡ {lesson.lesson_type}\n"

def teacher(lesson):
    return f"🧔 {lesson.teacher}\n"

def room(lesson):
    return f"🏫 {lesson.room}\n"

def online():
    return "🌐 Онлайн\n"
