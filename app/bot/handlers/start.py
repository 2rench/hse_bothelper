from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.database.user_repository import (
    get_user,
)

from app.bot.keyboards.group_years import (
    get_years_keyboard,
)

from app.bot.keyboards.menu import (
    get_main_menu,
)

from app.bot.keyboards.profile import (
    get_profile_keyboard,
)

router = Router()


@router.message(CommandStart())
async def start_handler(
    message: Message,
):

    if message.from_user is None:
        return

    user = get_user(
        message.from_user.id
    )

    if not user or not user["group_name"]:

        await message.answer(
            """
            <b>😎 привет!</b>\n\n🤖 Это — бот хелпер. Его основная задача — удобный просмотр расписания, <tg-spoiler>но это пока.</tg-spoiler>\nДля начала нужно выбрать группу и год.\n\n🏄‍♂️ Welcome
            """.strip(),
            reply_markup=get_years_keyboard(),
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
        reply_markup=get_profile_keyboard(),
    )

    await message.answer(
        "🏄‍♂️🏄‍♂️🏄‍♂️",
        reply_markup=get_main_menu(),
    )
