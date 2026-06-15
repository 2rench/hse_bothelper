from aiogram import Router
from aiogram.types import CallbackQuery

from app.bot.keyboards.groups import get_groups_keyboard
from app.database.user_repository import save_user_group
from app.bot.keyboards.menu import get_main_menu()

router = Router()


@router.callback_query(lambda c: c.data.startswith("year:"))
async def select_year(callback: CallbackQuery):

    year = callback.data.split(":")[1]

    await callback.message.edit_text(
        "Выберите группу:",
        reply_markup=get_groups_keyboard(year),
    )


@router.callback_query(lambda c: c.data.startswith("group:"))
async def select_group(callback: CallbackQuery):

    group = callback.data.split(":", 1)[1]

    save_user_group(
        telegram_id=callback.from_user.id,
        group_name=group,
    )

    await callback.message.edit_text(
        f"✅ Группа сохранена: {group}"
    )

    await callback.message.answer(
        "Теперь можно смотреть расписание 👇",
        reply_markup=get_main_menu(),
    )
