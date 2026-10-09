from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


def get_teachers_keyboard(
    teachers: list[str],
) -> InlineKeyboardMarkup:

    buttons = []

    for index, teacher in enumerate(teachers):
        buttons.append([
            InlineKeyboardButton(
                text=teacher,
                callback_data=f"teacher:{index}",
            )
        ])

    return InlineKeyboardMarkup(
        inline_keyboard=buttons
    )
