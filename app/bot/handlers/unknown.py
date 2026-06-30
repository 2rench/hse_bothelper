from aiogram import Router
from aiogram.types import Message

router = Router()


@router.message()
async def unknown_command(
    message: Message,
):
    await message.answer(
        "Стоп 🫷🏾\nКуда-то мы не туда\n\n"
        "Домой — /start"
    )
