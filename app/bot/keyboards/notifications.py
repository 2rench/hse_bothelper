from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


def get_notifications_keyboard(
    settings,
):

    schedule_updates = (
        settings["schedule_updates"]
        if settings
        else True
    )

    tomorrow_notifications = (
        settings["tomorrow_notifications"]
        if settings
        else True
    )

    updates = (
        "🟢 Общие уведомления"
        if schedule_updates
        else "🔴 Общие уведомления"
    )

    tomorrow = (
        "🟢 Напоминания о парах"
        if tomorrow_notifications
        else "🔴 Напоминания о парах"
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
