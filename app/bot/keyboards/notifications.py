from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


def get_notifications_keyboard(
    settings,
):

    updates = (
        "🟢 Общие уведомления"
        if settings.schedule_updates
        else
        "🔴 Общие уведомления"
    )

    tomorrow = (
        "🟢 Напоминания о парах"
        if settings.tomorrow_notifications
        else
        "🔴 Напоминания о парах"
    )

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=updates,
                    callback_data="toggle_updates",
                )
            ],
            [
                InlineKeyboardButton(
                    text=tomorrow,
                    callback_data="toggle_tomorrow",
                )
            ],
        ]
    )
