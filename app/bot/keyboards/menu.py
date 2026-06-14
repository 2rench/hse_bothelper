from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
)


def get_menu_keyboard():

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
                    text="💬 Поддержка"
                ),
            ],
        ],
        resize_keyboard=True,
    )
