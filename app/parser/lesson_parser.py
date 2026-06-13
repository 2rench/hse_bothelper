import re

ONLINE_KEYWORDS = [
    "teams",
    "zoom",
    "(онлайн[0])",
    "mts",
    "вебинар",
    "https://",
    "http://",
]

IGNORED_SUBJECTS = [
    "английский язык",
]

def is_online_lesson(text: str) -> bool:

    lower = text.lower()

    return any(
        keyword in lower
        for keyword in ONLINE_KEYWORDS
    )

def should_skip_lesson(subject: str) -> bool:

    subject = subject.lower()

    return any(
        ignored in subject
        for ignored in IGNORED_SUBJECTS
    )

def parse_lesson_text(
    text: str,
    is_shared: bool = False,
) -> dict:

    lines = [
        line.strip()
        for line in text.split("\n")
        if line.strip()
    ]

    if not lines:

        return {
            "subject": None,
            "teacher": None,
            "room": None,
            "building": None,
            "is_online": False,
            "skip": False,
            "lesson_type": None,
        }

    subject = lines[0]

    teacher = None
    room = None
    building = None

    if len(lines) >= 2:

        second_line = lines[1]

        # Teacher
        teacher_match = re.search(
            r"([А-ЯЁ][а-яё]+)\s+([А-ЯЁ]\.[А-ЯЁ]\.)",
            second_line,
        )

        if teacher_match:

            teacher = (
                f"{teacher_match.group(1)} "
                f"{teacher_match.group(2)}"
            )

        # Room/building
        room_match = re.search(
            r"\(([0-9]+)\[([0-9]+)\]",
            second_line,
        )

        if room_match:

            room = room_match.group(1)

            building = room_match.group(2)

    is_online = is_online_lesson(text)

    skip = should_skip_lesson(subject)

    lesson_type = (
        "Лекция"
        if is_shared
        else "Семинар"
    )

    return {
        "subject": subject,
        "teacher": teacher,
        "room": room,
        "building": building,
        "is_online": is_online,
        "skip": skip,
        "lesson_type": lesson_type,
    }
