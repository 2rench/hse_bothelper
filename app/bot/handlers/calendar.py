import os

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from app.database.user_repository import (
    get_or_create_calendar_token,
)


router = Router()


def build_keyboard(
    base_url: str,
    token: str,
) -> InlineKeyboardMarkup:
    """
    Собирает клавиатуру с кнопками календарей.
    """

    calendar_url = (
        f"{base_url}"
        f"/calendar/{token}.ics"
    )

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

    return InlineKeyboardMarkup(
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


def build_text(
    base_url: str,
    token: str,
) -> str:
    """
    Собирает текст сообщения с календарём.
    """

    calendar_url = (
        f"{base_url}"
        f"/calendar/{token}.ics"
    )

    return (
        "📅 <b>Твой календарь</b>\n\n"
        "Выбери календарь, в который хочешь "
        "добавить подписку:\n\n"
        "Также ссылку можно добавить вручную "
        "как подписку:\n\n"
        f"<code>{calendar_url}</code>\n\n"
        "Расписание будет обновляться "
        "после изменений в базе."
    )


async def send_calendar(
    message: Message,
):
    """
    Отправляет НОВОЕ сообщение с календарём.
    Используется для /calendar и текстовой кнопки.
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

    await message.answer(
        build_text(
            base_url,
            token,
        ),
        reply_markup=build_keyboard(
            base_url,
            token,
        ),
    )


async def edit_calendar(
    callback: CallbackQuery,
):
    """
    Редактирует сообщение, из которого
    была нажата кнопка «📅 Календарь» в профиле.
    """

    if callback.from_user is None:

        await callback.answer()

        return

    token = get_or_create_calendar_token(
        callback.from_user.id
    )

    if token is None:

        await callback.answer(
            "Пользователь не найден.",
            show_alert=True,
        )

        return

    base_url = os.getenv(
        "CALENDAR_BASE_URL"
    )

    if not base_url:

        await callback.answer(
            "Календарь пока не настроен.",
            show_alert=True,
        )

        return

    base_url = base_url.rstrip(
        "/"
    )

    if not isinstance(
        callback.message,
        Message,
    ):

        await callback.answer()

        return

    await callback.message.edit_text(
        build_text(
            base_url,
            token,
        ),
        reply_markup=build_keyboard(
            base_url,
            token,
        ),
    )

    await callback.answer()


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
async def calendar_text_handler(
    message: Message,
):
    await send_calendar(
        message
    )


@router.callback_query(
    F.data == "calendar"
)
async def calendar_callback_handler(
    callback: CallbackQuery,
):
    await edit_calendar(
        callback
    )
