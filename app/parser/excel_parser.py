from pathlib import Path
import json
import re

import xlrd

from app.parser.lesson_parser import parse_lesson_text

IGNORE_COLUMNS = {
"дни",
"пары",
}

def normalize_whitespace(text: str) -> str:

    text = re.sub(r"\n+", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)

    return text.strip()

def parse_day(raw_day: str) -> tuple[str, str]:

    parts = normalize_whitespace(raw_day).split("\n")

    if len(parts) >= 2:
        return parts[0], parts[1]

    return raw_day, ""


def parse_time(raw_time: str) -> tuple[str, str]:

    cleaned = normalize_whitespace(raw_time)

    parts = cleaned.split("\n")

    if len(parts) >= 2:
        return parts[0], parts[1]

    return "", cleaned


def get_merged_region(sheet, row_index, col_index):

    for merged in sheet.merged_cells:

        row_start, row_end, col_start, col_end = merged

        if (
            row_start <= row_index < row_end
            and
            col_start <= col_index < col_end
        ):
            return merged

    return None


def get_cell_value(sheet, row_index, col_index):

    value = sheet.cell_value(
        row_index,
        col_index,
    )

    if value:
        return value

    merged = get_merged_region(
        sheet,
        row_index,
        col_index,
    )

    if not merged:
        return ""

    row_start, _, col_start, _ = merged

    return sheet.cell_value(
        row_start,
        col_start,
    )


def is_underlined(sheet, row_index, col_index):

    cell = sheet.cell(
        row_index,
        col_index,
    )

    if cell.xf_index is None:
        return False

    try:

        xf = sheet.book.xf_list[cell.xf_index]

        font = sheet.book.font_list[
            xf.font_index
        ]

        return font.underlined != 0

    except Exception:
        return False


def create_lesson_record(
    group_name,
    current_day,
    current_date,
    lesson_number,
    lesson_time,
    sheet_name,
    lesson_text,
    lesson_info,
    lesson_type,
    schedule_name,
    schedule_type,
    schedule_key,
):

    return {
        "group": group_name,
        "day": current_day,
        "date": current_date,
        "lesson_number": lesson_number,
        "lesson_time": lesson_time,
        "sheet": sheet_name,

        "raw_text": lesson_text,

        "subject": lesson_info["subject"],
        "teacher": lesson_info["teacher"],
        "room": lesson_info["room"],
        "building": lesson_info["building"],

        "is_online": lesson_info["is_online"],
        "lesson_type": lesson_type,

        "schedule_name": schedule_name,
        "schedule_type": schedule_type,
        "schedule_key": schedule_key,
    }


def parse_excel(
    file_path: str,
    schedule_name: str,
    schedule_type: str,
    schedule_key: str,
) -> list[dict]:


    workbook = xlrd.open_workbook(
        file_path,
        formatting_info=True,
    )

    parsed_lessons: list[dict] = []

    # Чтобы не обрабатывать
    # shared area дважды
    processed_shared_cells = set()

    for sheet in workbook.sheets():

        print(f"Processing sheet: {sheet.name}")

        groups: dict[int, str] = {}

        GROUPS_ROW_INDEX = 2

        # Parse groups
        for col_index in range(sheet.ncols):

            value = get_cell_value(
                sheet,
                GROUPS_ROW_INDEX,
                col_index,
            )

            if not value:
                continue

            value = normalize_whitespace(
                str(value)
            )

            if value.lower() in IGNORE_COLUMNS:
                continue

            groups[col_index] = value

        current_day = None
        current_date = None

        # Parse lessons
        for row_index in range(3, sheet.nrows):

            day_cell = get_cell_value(
                sheet,
                row_index,
                0,
            )

            time_cell = get_cell_value(
                sheet,
                row_index,
                1,
            )

            if day_cell:

                current_day, current_date = parse_day(
                    str(day_cell)
                )

            if not time_cell:
                continue

            lesson_number, lesson_time = parse_time(
                str(time_cell)
            )

            for col_index, group_name in groups.items():

                lesson_cell = get_cell_value(
                    sheet,
                    row_index,
                    col_index,
                )

                if not lesson_cell:
                    continue

                lesson_text = normalize_whitespace(
                    str(lesson_cell)
                )

                if not lesson_text:
                    continue

                # Защита от дублей
                unique_key = (
                    row_index,
                    col_index,
                    lesson_text,
                )

                if unique_key in processed_shared_cells:
                    continue

                is_shared = is_underlined(
                    sheet,
                    row_index,
                    col_index,
                )

                lesson_info = parse_lesson_text(
                    lesson_text,
                    is_shared=is_shared,
                )

                if lesson_info["skip"]:
                    continue

                lesson_type = (
                    "Лекция"
                    if is_shared
                    else "Семинар"
                )

                # Обычная пара
                if not is_shared:

                    parsed_lessons.append(
                        create_lesson_record(
                            group_name,
                            current_day,
                            current_date,
                            lesson_number,
                            lesson_time,
                            sheet.name,
                            lesson_text,
                            lesson_info,
                            lesson_type,
                            schedule_name,
                            schedule_type,
                            schedule_key,
                        )
                    )

                    continue

                # Shared lesson logic

                shared_groups = [group_name]

                next_col = col_index + 1

                while next_col in groups:

                    next_value = sheet.cell_value(
                        row_index,
                        next_col,
                    )

                    next_is_underlined = is_underlined(
                        sheet,
                        row_index,
                        next_col,
                    )

                    # Если справа новая пара —
                    # все
                    if normalize_whitespace(
                        str(next_value)
                    ):
                        break

                    # underline закончился
                    if not next_is_underlined:
                        break

                    shared_groups.append(
                        groups[next_col]
                    )

                    processed_shared_cells.add(
                        (
                            row_index,
                            next_col,
                            lesson_text,
                        )
                    )

                    next_col += 1

                # Создаем lessons
                for shared_group in shared_groups:

                    parsed_lessons.append(
                        create_lesson_record(
                            group_name,
                            current_day,
                            current_date,
                            lesson_number,
                            lesson_time,
                            sheet.name,
                            lesson_text,
                            lesson_info,
                            lesson_type,
                            schedule_name,
                            schedule_type,
                            schedule_key,
                        )
                    )

                processed_shared_cells.add(
                    unique_key
                )

    return parsed_lessons

def export_to_json(
    lessons: list[dict],
    output_path: str,
) -> None:

    with open(
        output_path,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            lessons,
            file,
            ensure_ascii=False,
            indent=4,
        )


if __name__ == '__main__':


    FILE_PATH = Path(
        "files/schedule.xls"
    )

    OUTPUT_PATH = Path(
        "files/parsed_schedule.json"
    )

    if not FILE_PATH.exists():

        raise FileNotFoundError(
            f"File not found: "
            f"{FILE_PATH.absolute()}"
        )

    lessons = parse_excel(
        str(FILE_PATH),
        'TEST',
    )

    export_to_json(
        lessons=lessons,
        output_path=str(OUTPUT_PATH),
    )

    print(
        f"\nParsed lessons count: "
        f"{len(lessons)}"
    )

    print(
        f"JSON exported: "
        f"{OUTPUT_PATH.absolute()}"
    )
