from collections import defaultdict

from aiogram import Router
from aiogram.types import CallbackQuery

from app.database.user_repository import get_user_group
from app.database.session_repository import get_session_by_week
from app.services.schedule_service import get_week_lessons_by_number
from app.bot.services.formatter import format_lessons
from app.services.session_formatter import format_session_schedule


router = Router()


def _format_result(result) -> str:
    if isinstance(result, list):
        return "\n\n".join(str(item) for item in result)
    return str(result or "")


@router.callback_query(
    lambda c: c.data.startswith("open_week:")
)
async def open_week(callback: CallbackQuery):
    group = get_user_group(callback.from_user.id)

    if not group:
        await callback.answer(
            "Сначала выберите группу",
            show_alert=True,
        )
        return

    week = int(callback.data.replace("open_week:", ""))
    lessons = get_week_lessons_by_number(group, week)

    if not lessons:
        await callback.answer(
            "Расписание не найдено",
            show_alert=True,
        )
        return

    grouped = defaultdict(list)

    for lesson in lessons:
        grouped[(lesson.day, lesson.date)].append(lesson)

    for (day, date), day_lessons in grouped.items():
        text = f"<b>{day} — {date}</b>\n\n"

        formatted = format_lessons(
            day_lessons,
            telegram_id=callback.from_user.id,
        )

        text += _format_result(formatted)
        await callback.message.answer(text)

    await callback.answer()


@router.callback_query(
    lambda c: c.data.startswith("open_session:")
)
async def open_session(callback: CallbackQuery):
    group = get_user_group(callback.from_user.id)

    if not group:
        await callback.answer(
            "Сначала выберите группу",
            show_alert=True,
        )
        return

    week = int(callback.data.replace("open_session:", ""))
    lessons = get_session_by_week(group, week)

    if not lessons:
        await callback.answer(
            "Сессия не найдена",
            show_alert=True,
        )
        return

    messages = format_session_schedule(
        lessons,
        telegram_id=callback.from_user.id,
        week=week,
    )

    for message in messages:
        await callback.message.answer(message)

    await callback.answer()
