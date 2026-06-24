from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from app.database.group_repository import (
    get_groups_by_year,
)


def get_groups_keyboard(
    year: str,
):

    groups = get_groups_by_year(
        year
    )

    keyboard = []

    row = []

    for group in groups:

        row.append(
            InlineKeyboardButton(
                text=group,
                callback_data=f"group:{group}",
            )
        )

        if len(row) == 2:

            keyboard.append(row)

            row = []

    if row:

        keyboard.append(row)

    return InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )
