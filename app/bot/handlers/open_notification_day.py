from aiogram import Router
from aiogram.types import CallbackQuery

from app.database.user_repository import (
    get_user_group,
)

from app.services.schedule_service import (
    get_lessons_by_date,
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
        "open_day:"
    )
)
async def open_day(
    callback: CallbackQuery,
):

    group = get_user_group(
        callback.from_user.id
    )

    if not group:
        return

    date = callback.data.replace(
        "open_day:",
        "",
    )

    lessons = get_lessons_by_date(
        group,
        date,
    )

    text = (
        f"📚 {date}\n\n"
    )

    text += format_lessons(
        lessons
    )

    await callback.message.answer(
        text
    )

    await callback.answer()


@router.callback_query(
    lambda c:
    c.data.startswith(
        "open_session_day:"
    )
)
async def open_session_day(
    callback: CallbackQuery,
):

    group = get_user_group(
        callback.from_user.id
    )

    if not group:
        return

    date = callback.data.replace(
        "open_session_day:",
        "",
    )

    lessons = get_lessons_by_date(
        group,
        date,
    )

    text = (
        f"🎓 Экзамен\n"
        f"{date}\n\n"
    )

    text += format_lessons(
        lessons
    )

    await callback.message.answer(
        text
    )

    await callback.answer()
