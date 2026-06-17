from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


def get_profile_keyboard():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔄 Сменить группу",
                    callback_data="change_group",
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔄 Поддержка",
                    callback_data="help",
                )
            ]
        ]
    )
