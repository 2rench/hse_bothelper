from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
)

from app.database.schedule_repository import (
    has_sessions,
)


def get_main_menu():

    keyboard = [
        [
            KeyboardButton(
                text="📅 Сегодня"
            ),
            KeyboardButton(
                text="📆 Завтра"
            ),
        ],
    ]

    if has_sessions():

        keyboard.append(
            [
                KeyboardButton(
                    text="🗓 Неделя"
                ),
                KeyboardButton(
                    text="🎓 Сессия"
                ),
            ]
        )

        keyboard.append(
            [
                KeyboardButton(
                    text="🏃 Физ–ра"
                ),
                KeyboardButton(
                    text="🎾 Главная"
                ),
            ]
        )

    else:

        keyboard.append(
            [
                KeyboardButton(
                    text="🗓 Неделя"
                ),
                KeyboardButton(
                    text="🏃 Физ–ра"
                ),
            ]
        )

        keyboard.append(
            [
                KeyboardButton(
                    text="🎾 Главная"
                ),
            ]
        )

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        is_persistent=True,
    )
