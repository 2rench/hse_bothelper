from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.database.session_repository import (
    get_all_sessions,
)

from app.bot.keyboards.sessions import (
    get_sessions_keyboard,
)

router = Router()


@router.message(
    Command("sessions")
)
async def sessions_handler(
    message: Message,
):

    sessions = get_all_sessions()

    if not sessions:

        await message.answer(
            "Сессии не найдены"
        )

        return

    await message.answer(
        "🎓 Выберите сессию",
        reply_markup=get_sessions_keyboard(
            sessions
        ),
    )
