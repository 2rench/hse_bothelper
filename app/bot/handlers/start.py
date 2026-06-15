from app.database.user_repository import (
    get_user_group,
)

@router.message(CommandStart())
async def start_handler(message: Message):

    group = get_user_group(
        message.from_user.id
    )

    if group is None:

        await message.answer(
            "🎓 Добро пожаловать!\n\nВыберите курс:",
            reply_markup=get_years_keyboard(),
        )

        return

    await message.answer(
        f"🎓 HSE Bot\n\n"
        f"👤 ID: {message.from_user.id}\n"
        f"📚 Группа: {group}",
        reply_markup=get_main_menu(),
    )
