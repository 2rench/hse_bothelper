from pathlib import Path
import json
import re

import xlrd
import openpyxl

from app.parser.lesson_parser import parse_lesson_text
from app.database.group_repository import save_group

IGNORE_COLUMNS = {"дни", "пары"}


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


def _is_xlrd_sheet(sheet):
    return hasattr(sheet, "cell_value")


def _get_merged_cells(sheet):
    if _is_xlrd_sheet(sheet):
        return sheet.merged_cells
    else:
        merged = []
        for range_obj in sheet.merged_cells.ranges:
            merged.append((
                range_obj.min_row - 1,
                range_obj.max_row,
                range_obj.min_col - 1,
                range_obj.max_col
            ))
        return merged


def get_merged_region(sheet, row_index, col_index):
    for merged in _get_merged_cells(sheet):
        row_start, row_end, col_start, col_end = merged
        if row_start <= row_index < row_end and col_start <= col_index < col_end:
            return merged
    return None


def get_cell_value(sheet, row_index, col_index):
    if _is_xlrd_sheet(sheet):
        value = sheet.cell_value(row_index, col_index)
        if value:
            return value
        merged = get_merged_region(sheet, row_index, col_index)
        if not merged:
            return ""
        row_start, _, col_start, _ = merged
        return sheet.cell_value(row_start, col_start)
    else:
        cell = sheet.cell(row_index + 1, col_index + 1)
        value = cell.value
        if value is not None and value != "":
            return value
        merged = get_merged_region(sheet, row_index, col_index)
        if not merged:
            return ""
        row_start, _, col_start, _ = merged
        return sheet.cell(row_start + 1, col_start + 1).value


def is_underlined(sheet, row_index, col_index):
    if _is_xlrd_sheet(sheet):
        cell = sheet.cell(row_index, col_index)
        if cell.xf_index is None:
            return False
        try:
            xf = sheet.book.xf_list[cell.xf_index]
            font = sheet.book.font_list[xf.font_index]
            return font.underlined != 0
        except Exception:
            return False
    else:
        cell = sheet.cell(row_index + 1, col_index + 1)
        if cell.font and cell.font.underline:
            return bool(cell.font.underline)
        return False


def _open_workbook(file_path: str):
    path = Path(file_path)
    if path.suffix.lower() == ".xlsx":
        return openpyxl.load_workbook(file_path, data_only=True)
    else:
        return xlrd.open_workbook(file_path, formatting_info=True)


def _get_sheets(workbook):
    if hasattr(workbook, "sheets"):
        return workbook.sheets()
    else:
        return workbook.worksheets


def _get_nrows(sheet):
    if _is_xlrd_sheet(sheet):
        return sheet.nrows
    else:
        return sheet.max_row


def _get_ncols(sheet):
    if _is_xlrd_sheet(sheet):
        return sheet.ncols
    else:
        return sheet.max_column


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
    workbook = _open_workbook(file_path)
    parsed_lessons: list[dict] = []

    processed_shared_cells = set()

    for sheet in _get_sheets(workbook):
        print(f"Processing sheet: {sheet.name}")

        groups: dict[int, str] = {}
        GROUPS_ROW_INDEX = 2

        for col_index in range(_get_ncols(sheet)):
            value = get_cell_value(sheet, GROUPS_ROW_INDEX, col_index)
            if not value:
                continue
            value = normalize_whitespace(str(value))
            if value.lower() in IGNORE_COLUMNS:
                continue
            groups[col_index] = value
            save_group(value)

        current_day = None
        current_date = None

        for row_index in range(3, _get_nrows(sheet)):
            day_cell = get_cell_value(sheet, row_index, 0)
            time_cell = get_cell_value(sheet, row_index, 1)

            if day_cell:
                current_day, current_date = parse_day(str(day_cell))

            if not time_cell:
                continue

            lesson_number, lesson_time = parse_time(str(time_cell))

            for col_index, group_name in groups.items():
                lesson_cell = get_cell_value(sheet, row_index, col_index)
                if not lesson_cell:
                    continue

                lesson_text = normalize_whitespace(str(lesson_cell))
                if not lesson_text:
                    continue

                unique_key = (row_index, col_index, lesson_text)
                if unique_key in processed_shared_cells:
                    continue

                is_shared = is_underlined(sheet, row_index, col_index)

                lesson_info = parse_lesson_text(
                    lesson_text,
                    is_shared=is_shared,
                )

                if lesson_info["skip"]:
                    continue

                lesson_type = "Лекция" if is_shared else "Семинар"

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

                shared_groups = [group_name]
                next_col = col_index + 1

                while next_col in groups:
                    next_value = get_cell_value(sheet, row_index, next_col)
                    next_is_underlined = is_underlined(sheet, row_index, next_col)

                    if normalize_whitespace(str(next_value)):
                        break

                    if not next_is_underlined:
                        break

                    shared_groups.append(groups[next_col])
                    processed_shared_cells.add(
                        (row_index, next_col, lesson_text)
                    )
                    next_col += 1

                for shared_group in shared_groups:
                    parsed_lessons.append(
                        create_lesson_record(
                            shared_group,
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

                processed_shared_cells.add(unique_key)

    return parsed_lessons


def export_to_json(
    lessons: list[dict],
    output_path: str,
) -> None:
    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(lessons, file, ensure_ascii=False, indent=4)