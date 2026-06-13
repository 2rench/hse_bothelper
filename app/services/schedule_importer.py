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
):

    schedule_name = Path(
        file_path
    ).stem

    try:

        lessons = parse_excel(
            file_path=file_path,
            schedule_name=schedule_name,
        )

    except xlrd.biffh.XLRDError:

        print(
            f"INVALID XLS: {file_path}"
        )

        return False

    load_lessons(
        lessons
    )

    return True
