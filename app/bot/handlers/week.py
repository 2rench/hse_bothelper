from collections import defaultdict

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.services.schedule_service import (
    get_week_lessons,
)

from app.database.user_repository import (
    get_user_group,
)

from app.bot.keyboards.group_years import (
    get_years_keyboard,
)

from app.bot.services.formatter import (
    format_lessons,
)

router = Router()


@router.message(Command("week"))
async def week_handler(message: Message):

    group = get_user_group(
        message.from_user.id
    )

    if group is None:

        await message.answer(
            "Выбери группу",
            reply_markup=get_years_keyboard(),
        )

        return

    lessons = get_week_lessons(group)

    if not lessons:

        await message.answer(
            "Расписание не найдено"
        )

        return

    grouped = defaultdict(list)

    for lesson in lessons:

        grouped[
            (lesson.day, lesson.date)
        ].append(lesson)

    text = (
        f"📚 Расписание недели\n"
        f"🧭 Группа: {group}\n\n"
    )

    for (day, date), day_lessons in grouped.items():

        text += (
            f"━━━━━━━━━━━━\n"
            f"📅 {day} — {date}\n\n"
        )

        text += format_lessons(
            day_lessons
        )

        text += "\n"

    msg = await message.answer(text)

    try:
        await message.bot.unpin_all_chat_messages(
            message.chat.id
        )
    except:
        pass

    try:
        await message.bot.pin_chat_message(
            chat_id=message.chat.id,
            message_id=msg.message_id,
        )
    except:
        pass


@router.message(
    lambda m: m.text == "🗓 Неделя"
)
async def week_button(
    message: Message,
):
    await week_handler(message)
