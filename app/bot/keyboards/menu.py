from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
)


def get_main_menu(
    has_session: bool = False,
):

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

    # если в бд есть сессии, то выводим кнопку
    if has_session:

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
    )
