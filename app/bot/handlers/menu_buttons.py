from aiogram import Router
from aiogram.types import Message

router = Router()


@router.message(
    lambda m: m.text == "📅 Сегодня"
)
async def today_button(
    message: Message,
):
    await message.answer(
        "/today"
    )


@router.message(
    lambda m: m.text == "📆 Завтра"
)
async def tomorrow_button(
    message: Message,
):
    await message.answer(
        "/tomorrow"
    )


@router.message(
    lambda m: m.text == "🗓 Неделя"
)
async def week_button(
    message: Message,
):
    await message.answer(
        "/week"
    )


@router.message(
    lambda m: m.text == "🎓 Сессия"
)
async def sessions_button(
    message: Message,
):
    await message.answer(
        "/sessions"
    )

@router.message(
    lambda m: m.text == "💬 Поддержка"
)
async def support_handler(
    message: Message,
):

    await message.answer(
        "💬 Поддержка\n\n"
        "@2rench"
    )

@router.message(
    lambda m: m.text == "⚙️ Уведомления"
)
async def notifications_handler(
    message: Message,
):
    await message.answer(
        "Открываю настройки..."
    )
