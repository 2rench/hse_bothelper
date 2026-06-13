from aiogram import Router
from aiogram.types import CallbackQuery

from app.database.user_repository import (
    get_user_group,
)

from app.database.session_repository import (
    get_session_by_week,
)

from app.services.schedule_service import (
    get_week_lessons_by_number,
)

from app.bot.services.formatter import (
    format_lessons,
)

router = Router()


@router.callback_query(
    lambda c:
    c.data.startswith(
        "open_week:"
    )
)
async def open_week(
    callback: CallbackQuery,
):

    group = get_user_group(
        callback.from_user.id
    )

    if not group:

        await callback.answer(
            "Сначала выберите группу",
            show_alert=True,
        )
        return

    week = int(
        callback.data.replace(
            "open_week:",
            "",
        )
    )

    lessons = (
        get_week_lessons_by_number(
            group,
            week,
        )
    )

    if not lessons:

        await callback.answer(
            "Расписание не найдено",
            show_alert=True,
        )
        return

    text = (
        f"📚 Неделя №{week}\n\n"
    )

    text += format_lessons(
        lessons,
        group_by_day=True,
    )

    await callback.message.answer(
        text
    )

    await callback.answer()


@router.callback_query(
    lambda c:
    c.data.startswith(
        "open_session:"
    )
)
async def open_session(
    callback: CallbackQuery,
):

    group = get_user_group(
        callback.from_user.id
    )

    if not group:

        await callback.answer(
            "Сначала выберите группу",
            show_alert=True,
        )
        return

    week = int(
        callback.data.replace(
            "open_session:",
            "",
        )
    )

    lessons = get_session_by_week(
        group,
        week,
    )

    if not lessons:

        await callback.answer(
            "Сессия не найдена",
            show_alert=True,
        )
        return

    text = (
        f"🎓 Сессия (неделя №{week})\n\n"
    )

    text += format_lessons(
        lessons,
        group_by_day=True,
    )

    await callback.message.answer(
        text
    )

    await callback.answer()
