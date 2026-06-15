from aiogram import Router
from aiogram.types import Message

from app.database.user_repository import (
    get_user,
)

from app.bot.keyboards.menu import (
    get_main_menu,
)

router = Router()


@router.message(
    lambda m: m.text == "🏠 Главная"
)
async def home_handler(
    message: Message,
):

    if message.from_user is None:
        return

    user = get_user(
        message.from_user.id
    )

    if not user:

        await message.answer(
            "Сначала выберите группу через /start"
        )

        return

    updates = (
        "🟢 ВКЛ"
        if user["schedule_updates"]
        else "🔴 ВЫКЛ"
    )

    tomorrow = (
        "🟢 ВКЛ"
        if user["tomorrow_notifications"]
        else "🔴 ВЫКЛ"
    )

    text = (
        "🎓 HSE Bot\n\n"
        f"👤 ID: {message.from_user.id}\n"
        f"📚 Группа: {user['group_name']}\n\n"
        f"🔔 Изменения: {updates}\n"
        f"🌙 Напоминания: {tomorrow}"
    )

    await message.answer(
        text,
        reply_markup=get_main_menu(),
    )
