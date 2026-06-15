from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
)


def get_main_menu():

    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="📅 Сегодня"
                ),
                KeyboardButton(
                    text="📆 Завтра"
                ),
            ],
            [
                KeyboardButton(
                    text="🗓 Неделя"
                ),
                KeyboardButton(
                    text="🎓 Сессия"
                ),
            ],
            [
                KeyboardButton(
                    text="⚙️ Уведомления"
                ),
                KeyboardButton(
                    text="🏠 Главная"
                ),
            ],
        ],
        resize_keyboard=True,
    )
