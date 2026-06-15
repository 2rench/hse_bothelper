from aiogram import Router
from aiogram.filters import Command
from aiogram.types import (
    Message,
    CallbackQuery,
)

from app.database.user_repository import (
    get_user,
    toggle_schedule_updates,
    toggle_tomorrow_notifications,
)

from app.bot.keyboards.notifications import (
    get_notifications_keyboard,
)

router = Router()


@router.message(
    Command("notifications")
)
async def notifications_handler(
    message: Message,
):

    settings = get_user(
        message.from_user.id
    )

    await message.answer(
        "🔔 Настройки уведомлений",
        reply_markup=
        get_notifications_keyboard(
            settings
        ),
    )


@router.message(
    lambda m: m.text == "⚙️ Уведомления"
)
async def notifications_button(
    message: Message,
):
    await notifications_handler(
        message
    )


@router.callback_query(
    lambda c:
    c.data == "toggle_updates"
)
async def toggle_updates(
    callback: CallbackQuery,
):

    toggle_schedule_updates(
        callback.from_user.id
    )

    settings = get_user(
        callback.from_user.id
    )

    await callback.message.edit_reply_markup(
        reply_markup=get_notifications_keyboard(settings)
    )

    await callback.answer()


@router.callback_query(
    lambda c:
    c.data == "toggle_tomorrow"
)
async def toggle_tomorrow(
    callback: CallbackQuery,
):

    toggle_tomorrow_notifications(
        callback.from_user.id
    )

    settings = get_user(
        callback.from_user.id
    )

    await callback.message.edit_reply_markup(
        reply_markup=get_notifications_keyboard(settings)
    )

    await callback.answer()
