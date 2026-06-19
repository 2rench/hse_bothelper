from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
)


def admin_keyboard():

    builder = InlineKeyboardBuilder()

    builder.button(
        text="📢 Рассылка",
        callback_data="create_broadcast"
    )

    return builder.as_markup()


def confirm_keyboard():

    builder = InlineKeyboardBuilder()

    builder.button(
        text="✅ Отправить",
        callback_data="broadcast_yes"
    )

    builder.button(
        text="❌ Отмена",
        callback_data="broadcast_no"
    )

    return builder.as_markup()
