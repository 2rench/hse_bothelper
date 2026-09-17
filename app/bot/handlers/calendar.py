import os

from aiogram import Router
from aiogram.types import (
    CallbackQuery,
)

from app.database.user_repository import (
    get_or_create_calendar_token,
)


router = Router()


@router.callback_query(
    lambda c:
    c.data == "calendar"
)
async def calendar_handler(
    callback: CallbackQuery,
):

    if callback.from_user is None:

        return

    token = get_or_create_calendar_token(
        callback.from_user.id
    )

    if token is None:

        await callback.answer(
            "Пользователь не найден",
            show_alert=True,
        )

        return

    base_url = os.getenv(
        "CALENDAR_BASE_URL"
    )

    if not base_url:

        await callback.answer(
            "Календарь пока не настроен",
            show_alert=True,
        )

        return

    base_url = base_url.rstrip(
        "/"
    )

    url = (
        f"{base_url}"
        f"/calendar/{token}.ics"
    )

    await callback.message.answer(
        "📅 <b>Календарь</b>\n\n"
        "Добавьте эту ссылку в свой календарь "
        "как подписку:\n\n"
        f"<code>{url}</code>\n\n"
        "Расписание будет обновляться "
        "автоматически после изменения "
        "данных в боте."
    )

    await callback.answer()
