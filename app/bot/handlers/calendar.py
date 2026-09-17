import os

from urllib.parse import urlparse

from aiogram import Router
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


def build_webcal_url(https_url: str) -> str:
    """
    Преобразует https://... в webcal://...
    Такой формат большинство календарей
    (iOS, macOS, Outlook) открывают сразу
    как подписку.
    """
    parsed = urlparse(https_url)
    return parsed._replace(scheme="webcal").geturl()


async def send_calendar(
    message: Message,
):
    """
    Отправляет пользователю ссылку на календарь
    и кнопки для подписки в разных календарях.
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

    webcal_url = build_webcal_url(
        calendar_url
    )

    # Google Calendar принимает ссылку на .ics
    # через параметр src
    google_url = (
        "https://calendar.google.com/calendar/r?"
        "cid=webcal%3A%2F%2F"
        + urlparse(calendar_url)
        .netloc
        + urlparse(calendar_url).path
    )

    # Outlook Web
    outlook_url = (
        "https://outlook.live.com/calendar/0/"
        "addcalendar/subscribe?"
        f"url={webcal_url}"
    )

    # Yandex Calendar
    yandex_url = (
        "https://calendar.yandex.ru/"
        f"?webcal={webcal_url}"
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🍎 Apple / iOS",
                    url=webcal_url,
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
    lambda message: message.text == "📅 Календарь"
)
async def calendar_button_handler(
    message: Message,
):
    await send_calendar(
        message
    )
