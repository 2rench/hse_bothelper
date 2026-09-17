import os

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.database.user_repository import (
    get_or_create_calendar_token,
)


router = Router()


@router.message(
    Command("calendar")
)
async def calendar_handler(
    message: Message,
):

    if message.from_user is None:
        return

    token = get_or_create_calendar_token(
        message.from_user.id
    )

    if token is None:

        await message.answer(
            "Пользователь не найден."
        )

        return

    base_url = os.getenv(
        "CALENDAR_BASE_URL"
    )

    if not base_url:

        await message.answer(
            "Календарь пока не настроен."
        )

        return

    base_url = base_url.rstrip(
        "/"
    )

    calendar_url = (
        f"{base_url}"
        f"/calendar/{token}.ics"
    )

    await message.answer(
        "📅 <b>Твой календарь</b>\n\n"
        "Добавь эту ссылку в приложение "
        "календаря как подписку:\n\n"
        f"<code>{calendar_url}</code>\n\n"
        "Расписание будет обновляться "
        "после изменений в базе."
    )
