from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.bot.keyboards.group_years import (
    get_years_keyboard,
)
from app.bot.keyboards.menu import (
    get_main_menu,
)

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):

    await message.answer(
        f"🎓 HSE Bot\n\n"
        f"👤 ID: {message.from_user.id}\n"
        f"📚 Группа: {group}",
        reply_markup=get_main_menu(),
    )
