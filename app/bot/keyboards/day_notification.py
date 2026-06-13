from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


def get_day_keyboard(
    date: str,
    is_session: bool,
):

    callback = (
        f"open_session_day:{date}"
        if is_session
        else
        f"open_day:{date}"
    )

    text = (
        "🎓 Открыть экзамен"
        if is_session
        else
        "📖 Открыть расписание"
    )

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=text,
                    callback_data=callback,
                )
            ]
        ]
    )
