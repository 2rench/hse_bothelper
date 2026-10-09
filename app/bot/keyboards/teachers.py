from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

PAGE_SIZE = 10


def get_teachers_keyboard(
    teachers: list[str],
    page: int = 0,
) -> InlineKeyboardMarkup:
    total = len(teachers)
    total_pages = max(1, (total + PAGE_SIZE - 1) // PAGE_SIZE)
    page = max(0, min(page, total_pages - 1))

    start = page * PAGE_SIZE
    end = start + PAGE_SIZE

    keyboard: list[list[InlineKeyboardButton]] = []

    for i in range(start, end):
        if i >= total:
            break

        keyboard.append([
            InlineKeyboardButton(
                text=teachers[i],
                callback_data=f"teacher:{i}",
            )
        ])

    nav_row: list[InlineKeyboardButton] = []

    if page > 0:
        nav_row.append(
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data=f"teachers_page:{page - 1}",
            )
        )

    nav_row.append(
        InlineKeyboardButton(
            text=f"{page + 1}/{total_pages}",
            callback_data="teachers_noop",
        )
    )

    if page < total_pages - 1:
        nav_row.append(
            InlineKeyboardButton(
                text="Вперёд ➡️",
                callback_data=f"teachers_page:{page + 1}",
            )
        )

    keyboard.append(nav_row)

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
