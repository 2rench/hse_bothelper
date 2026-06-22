from aiogram import Router
from aiogram.types import (
    Message,
    CallbackQuery,
)

from app.database.user_repository import (
    get_user_group,
)

from app.database.session_repository import (
    get_session_lessons,
)

from app.bot.services.formatter import (
    format_lessons,
)

router = Router()


@router.callback_query(
    lambda c:
    c.data.startswith(
        "session:"
    )
)
async def show_session(
    callback: CallbackQuery,
):

    group = get_user_group(
        callback.from_user.id
    )

    if not group:

        await callback.answer(
            "Выберите группу"
        )
        return

    session_name = (
        callback.data.replace(
            "session:",
            "",
        )
    )

    lessons = (
        get_session_lessons(
            group,
            session_name,
        )
    )

    if not lessons:

        await callback.message.edit_text(
            "Для вашей группы "
            "в этой сессии "
            "ничего нет"
        )

        return

    text = (
        f"🎓 {session_name}\n\n"
    )

    text += format_lessons(
        lessons,
        group_by_day=True,
    )

    await callback.message.edit_text(
        text
    )

    await callback.answer()
    @router.message(
        lambda m: m.text == "🎓 Сессия"
    )
    async def sessions_button(
        message: Message,
    ):
        await sessions_handler(
            message
        )
