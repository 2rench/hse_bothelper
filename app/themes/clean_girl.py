def no_lessons():
    return "Сегодня свободно ☁️"

def lessons_count(count):
    return f"☁️ {count} занятий"

def lesson_header(lesson):
    return f"{lesson.lesson_time}\n"

def subject(lesson):
    return f"{lesson.subject}\n"

def lesson_type(lesson):
    return f"{lesson.lesson_type}\n"

def teacher(lesson):
    return f"{lesson.teacher}\n"

def room(lesson):
    return f"{lesson.room}\n"

def online():
    return "online\n"
