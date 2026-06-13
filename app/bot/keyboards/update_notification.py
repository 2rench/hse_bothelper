from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


def get_update_keyboard(
    week: int,
    is_session: bool,
):

    if is_session:

        callback = f"open_session:{week}"
        text = "🎓 Открыть сессию"

    else:

        callback = f"open_week:{week}"
        text = "📚 Открыть расписание"

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
