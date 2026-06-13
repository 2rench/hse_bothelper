from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.bot.keyboards.group_years import (
    get_years_keyboard,
)
from app.bot.keyboards.menu import (
    get_menu_keyboard,
)

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):

    await message.answer(
        "Выбери год поступления:",
        reply_markup=get_years_keyboard(),
    )