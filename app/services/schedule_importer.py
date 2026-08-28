from pathlib import Path

import xlrd

from app.parser.excel_parser import (
    parse_excel,
)

from app.services.lesson_loader import (
    load_lessons,
)


def import_schedule(
    file_path: str,
    schedule_type: str,
    schedule_key: str,
):

    schedule_name = Path(
        file_path
    ).stem

    print(
        "IMPORT START:",
        file_path,
    )

    print(
        "SCHEDULE NAME:",
        schedule_name,
    )

    print(
        "SCHEDULE TYPE:",
        schedule_type,
    )

    print(
        "SCHEDULE KEY:",
        schedule_key,
    )

    try:

        lessons = parse_excel(
            file_path=file_path,
            schedule_name=schedule_name,
            schedule_type=schedule_type,
            schedule_key=schedule_key,
        )

        print(
            "PARSE SUCCESS"
        )

        print(
            "LESSONS PARSED:",
            len(lessons),
        )

        if lessons:

            print(
                "FIRST LESSON:",
                lessons[0],
            )

    except xlrd.biffh.XLRDError:

        print(
            f"INVALID XLS: {file_path}"
        )

        return False

    except Exception as error:

        print(
            "PARSE ERROR:",
            repr(error),
        )

        return False

    try:

        load_lessons(
            lessons
        )

        print(
            "LESSONS LOADED:",
            len(lessons),
        )

    except Exception as error:

        print(
            "LOAD LESSONS ERROR:",
            repr(error),
        )

        return False

    print(
        "IMPORT FINISHED:",
        schedule_name,
    )

    return True