from aiogram import Router
from aiogram.types import Message

from app.database.user_repository import (
    get_user,
    get_user_group,
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

    user = get_user(
        message.from_user.id
    )

    group = get_user_group(
        message.from_user.id
    ) or "не выбрана"

    updates = (
        "🟢 ВКЛ"
        if user and user.schedule_updates
        else "🔴 ВЫКЛ"
    )

    tomorrow = (
        "🟢 ВКЛ"
        if user and user.tomorrow_notifications
        else "🔴 ВЫКЛ"
    )

    text = (
        "🎓 HSE Bot\n\n"
        f"👤 ID: {message.from_user.id}\n"
        f"📚 Группа: {group}\n\n"
        f"🔔 Изменения: {updates}\n"
        f"🌙 Напоминания: {tomorrow}"
    )

    await message.answer(
        text,
        reply_markup=get_main_menu(),
    )
