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


TEACHER_PATTERN = re.compile(
    r"([А-ЯЁ][а-яё]+)\s+([А-ЯЁ]\.[А-ЯЁ]\.)"
)


ROOM_PATTERN = re.compile(
    r"\(?([0-9]+)\[([0-9]+)\]"
)


def is_online_lesson(
    text: str,
) -> bool:

    lower = text.lower()

    return any(
        keyword in lower
        for keyword in ONLINE_KEYWORDS
    )


def should_skip_lesson(
    subject: str,
) -> bool:

    subject = subject.lower()

    return any(
        ignored in subject
        for ignored in IGNORED_SUBJECTS
    )


def _parse_single_lesson(
    lines: list[str],
    is_shared: bool = False,
) -> dict:

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

    for line in lines[1:]:

        teacher_match = TEACHER_PATTERN.search(
            line
        )

        if teacher_match and teacher is None:

            teacher = (
                f"{teacher_match.group(1)} "
                f"{teacher_match.group(2)}"
            )

        room_match = ROOM_PATTERN.search(
            line
        )

        if room_match and room is None:

            room = room_match.group(1)
            building = room_match.group(2)

    full_text = "\n".join(lines)

    is_online = is_online_lesson(
        full_text
    )

    skip = should_skip_lesson(
        subject
    )

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


def parse_lesson_texts(
    text: str,
    is_shared: bool = False,
) -> list[dict]:

    lines = [
        line.strip()
        for line in text.split("\n")
        if line.strip()
    ]

    if not lines:

        return []

    # Сначала ищем все строки преподавателей.
    # Если преподаватель только один,
    # это обычная одиночная пара.
    teacher_indexes = []

    for index, line in enumerate(lines):

        if TEACHER_PATTERN.search(line):

            teacher_indexes.append(index)

    if len(teacher_indexes) <= 1:

        lesson_info = _parse_single_lesson(
            lines,
            is_shared=is_shared,
        )

        if lesson_info["skip"]:

            return []

        return [
            lesson_info
        ]

    lessons = []

    first_teacher_index = teacher_indexes[0]

    current_block = lines[
        :first_teacher_index + 1
    ]

    for index in range(
        first_teacher_index + 1,
        len(lines),
    ):

        line = lines[index]

        # URL / онлайн-ссылка относится
        # к предыдущей паре.
        if (
            "http://" in line.lower()
            or
            "https://" in line.lower()
            or
            "telemost.yandex.ru" in line.lower()
            or
            "hse.mts-link.ru" in line.lower()
        ):

            current_block.append(
                line
            )

            continue

        # После строки преподавателя
        # следующая обычная строка =
        # начало следующей пары.
        previous_line_is_teacher = bool(
            TEACHER_PATTERN.search(
                lines[index - 1]
            )
        )

        if previous_line_is_teacher:

            lesson_info = _parse_single_lesson(
                current_block,
                is_shared=is_shared,
            )

            if not lesson_info["skip"]:

                lessons.append(
                    lesson_info
                )

            current_block = [
                line
            ]

            continue

        current_block.append(
            line
        )

    if current_block:

        lesson_info = _parse_single_lesson(
            current_block,
            is_shared=is_shared,
        )

        if not lesson_info["skip"]:

            lessons.append(
                lesson_info
            )

    return lessons


def parse_lesson_text(
    text: str,
    is_shared: bool = False,
) -> dict:

    lessons = parse_lesson_texts(
        text,
        is_shared=is_shared,
    )

    if not lessons:

        return {
            "subject": None,
            "teacher": None,
            "room": None,
            "building": None,
            "is_online": False,
            "skip": False,
            "lesson_type": None,
        }

    return lessons[0]
