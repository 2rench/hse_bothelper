def no_lessons():
    return "status=FREE"

def lessons_count(count):
    return f"tasks={count}"

def lesson_header(lesson):
    return (
        f"BEGIN {lesson.lesson_time}\n"
    )

def subject(lesson):
    return f"module={lesson.subject}\n"

def lesson_type(lesson):
    return f"type={lesson.lesson_type}\n"

def teacher(lesson):
    return f"mentor={lesson.teacher}\n"

def room(lesson):
    return f"location={lesson.room}\n"

def online():
    return "remote=True\n"
