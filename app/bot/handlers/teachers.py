from datetime import datetime

from aiogram import Router
from aiogram.types import (
    CallbackQuery,
    Message,
)

from app.database.teacher_repository import (
    get_today_teachers,
    get_teacher_lessons_today,
)

from app.bot.keyboards.teachers import (
    get_teachers_keyboard,
)


router = Router()

teacher_cache: dict[int, list[str]] = {}


@router.callback_query(
    lambda c: c.data == "teachers_today"
)
async def teachers_today_handler(
    callback: CallbackQuery,
):
    teachers = get_today_teachers()

    if not teachers:
        await callback.message.answer(
            "Сегодня преподавателей с парами не найдено."
        )
        await callback.answer()
        return

    teacher_cache[callback.from_user.id] = teachers

    await callback.message.answer(
        "👨‍🏫 <b>Преподаватели сегодня</b>\n\n"
        "Выбери преподавателя:",
        reply_markup=get_teachers_keyboard(teachers, page=0),
    )

    await callback.answer()


@router.callback_query(
    lambda c: c.data.startswith("teachers_page:")
)
async def teachers_page_handler(
    callback: CallbackQuery,
):
    try:
        page = int(callback.data.split(":", 1)[1])
    except ValueError:
        await callback.answer()
        return

    teachers = teacher_cache.get(callback.from_user.id)

    if not teachers:
        await callback.answer(
            "Список устарел. Открой его заново.",
            show_alert=True,
        )
        return

    try:
        await callback.message.edit_reply_markup(
            reply_markup=get_teachers_keyboard(teachers, page=page),
        )
    except Exception:
        # на случай, если сообщение слишком старое / не изменилось
        await callback.message.answer(
            "👨‍🏫 <b>Преподаватели сегодня</b>\n\n"
            "Выбери преподавателя:",
            reply_markup=get_teachers_keyboard(teachers, page=page),
        )

    await callback.answer()


@router.callback_query(
    lambda c: c.data == "teachers_noop"
)
async def teachers_noop_handler(
    callback: CallbackQuery,
):
    await callback.answer()


@router.callback_query(
    lambda c: c.data.startswith("teacher:")
)
async def teacher_schedule_handler(
    callback: CallbackQuery,
):
    try:
        index = int(callback.data.split(":", 1)[1])
        teachers = teacher_cache.get(
            callback.from_user.id,
            [],
        )
        teacher = teachers[index]
    except (ValueError, IndexError):
        await callback.answer(
            "Список устарел. Открой его заново.",
            show_alert=True,
        )
        return

    lessons = get_teacher_lessons_today(teacher)

    if not lessons:
        await callback.answer(
            "Сегодня пар не найдено.",
            show_alert=True,
        )
        return

    text = f"👨‍🏫 <b>{teacher}</b>\n"
    text += f"📅 {datetime.now().strftime('%d.%m.%Y')}\n\n"

    for lesson in lessons:
        text += (
            f"🕒 <b>{lesson.lesson_time}</b>\n"
            f"📚 {lesson.subject or 'Предмет не указан'}\n"
            f"{lesson.group_name}, "
        )

        if lesson.room:
            text += f"{lesson.room}"

            if lesson.building:
                text += f" [{lesson.building}]"

            text += "\n"

        if lesson.is_online:
            text += "🌐 Онлайн\n"

        text += "\n"

    await callback.message.answer(text.strip())
    await callback.answer()
    