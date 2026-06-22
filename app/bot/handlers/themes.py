from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.bot.keyboards.themes import (
    get_themes_keyboard,
    get_girls_themes_keyboard,
    get_boys_themes_keyboard,
)

from app.database.user_repository import (
    set_theme,
)

router = Router()


@router.callback_query(
    F.data == "themes"
)
async def show_themes(
    callback: CallbackQuery,
):

    await callback.message.edit_text(
        "🎨 Выбери категорию:",
        reply_markup=get_themes_keyboard()
    )

    await callback.answer()


@router.callback_query(
    F.data == "themes_girls"
)
async def girls_themes(
    callback: CallbackQuery,
):

    await callback.message.edit_text(
        "👩 Темы для девушек:",
        reply_markup=get_girls_themes_keyboard()
    )

    await callback.answer()


@router.callback_query(
    F.data == "themes_boys"
)
async def boys_themes(
    callback: CallbackQuery,
):

    await callback.message.edit_text(
        "👨 Темы для парней:",
        reply_markup=get_boys_themes_keyboard()
    )

    await callback.answer()


@router.callback_query(
    F.data.startswith("theme_")
)
async def choose_theme(
    callback: CallbackQuery,
):

    theme = callback.data.replace(
        "theme_",
        ""
    )

    set_theme(
        callback.from_user.id,
        theme
    )

    await callback.answer(
        "✅ Тема сохранена"
    )

    await callback.message.edit_text(
        "🎉 Тема успешно изменена!"
    )
