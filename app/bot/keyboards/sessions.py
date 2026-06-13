from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


def get_sessions_keyboard(
    sessions: list[str],
):

    buttons = []

    for session in sessions:

        buttons.append(
            [
                InlineKeyboardButton(
                    text=session,
                    callback_data=(
                        f"session:{session}"
                    )[:64],
                )
            ]
        )

    return InlineKeyboardMarkup(
        inline_keyboard=buttons
    )
