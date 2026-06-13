from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
)


def get_menu_keyboard():

    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="/today"
                ),

                KeyboardButton(
                    text="/tomorrow"
                ),
            ],
            [
                KeyboardButton(
                    text="/week"
                ),
            ],
        ],
        resize_keyboard=True,
    )
