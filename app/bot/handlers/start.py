from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.database.user_repository import (
    get_user,
    get_user_group,
)

from app.bot.keyboards.group_years import (
    get_years_keyboard,
)

from app.bot.keyboards.menu import (
    get_main_menu,
)

router = Router()


@router.message(CommandStart())
async def start_handler(
    message: Message,
):

    group = get_user_group(
        message.from_user.id
    )

    if group is None:

        await message.answer(
            "🎓 Привет!\n\nВыбери курс:",
            reply_markup=get_years_keyboard(),
        )

        return

    user = get_user(
        message.from_user.id
    )

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
