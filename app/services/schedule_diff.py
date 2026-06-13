def lessons_key(lesson):

    return (
        lesson.group_name,
        lesson.date,
        lesson.lesson_number,
        lesson.subject,
        lesson.teacher,
        lesson.room,
    )