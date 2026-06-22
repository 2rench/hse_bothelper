from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
)


from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


def admin_keyboard():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📢 Рассылка",
                    callback_data="admin_broadcast",
                )
            ],
            [
                InlineKeyboardButton(
                    text="📊 Статистика",
                    callback_data="admin_stats",
                )
            ],
        ]
    )



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
