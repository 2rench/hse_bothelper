import os

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from app.database.user_repository import (
    get_or_create_calendar_token,
)


router = Router()


async def send_calendar(
    message: Message,
):
    """
    Отправляет пользователю сообщение
    с кнопками для подписки на календарь.
    """

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

    # https → редирект на webcal://
    # (для Apple, iOS, macOS)
    subscribe_url = (
        f"{base_url}"
        f"/calendar/{token}/subscribe"
    )

    google_url = (
        "https://calendar.google.com/calendar/r?"
        f"cid={calendar_url}"
    )

    outlook_url = (
        "https://outlook.live.com/calendar/0/"
        f"addcalendar/subscribe?url={calendar_url}"
    )

    yandex_url = (
        "https://calendar.yandex.ru/"
        f"?webcal={calendar_url}"
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🍎 Apple / iOS",
                    url=subscribe_url,
                ),
            ],
            [
                InlineKeyboardButton(
                    text="📆 Google Calendar",
                    url=google_url,
                ),
            ],
            [
                InlineKeyboardButton(
                    text="📧 Outlook",
                    url=outlook_url,
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🟡 Яндекс.Календарь",
                    url=yandex_url,
                ),
            ],
            [
                InlineKeyboardButton(
                    text="📅 Открыть .ics",
                    url=calendar_url,
                ),
            ],
        ]
    )

    await message.answer(
        "📅 <b>Твой календарь</b>\n\n"
        "Выбери календарь, в который хочешь "
        "добавить подписку:\n\n"
        "Также ссылку можно добавить вручную "
        "как подписку:\n\n"
        f"<code>{calendar_url}</code>\n\n"
        "Расписание будет обновляться "
        "после изменений в базе.",
        reply_markup=keyboard,
    )


@router.message(
    Command("calendar")
)
async def calendar_handler(
    message: Message,
):
    await send_calendar(
        message
    )


@router.message(
    F.text == "📅 Календарь"
)
async def calendar_button_handler(
    message: Message,
):
    await send_calendar(
        message
    )
