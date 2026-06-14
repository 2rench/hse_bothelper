from datetime import datetime

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.services.schedule_service import (
    get_lessons_by_date,
    get_current_study_date,
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


@router.message(Command("today"))
async def today_handler(message: Message):

    group = get_user_group(
        message.from_user.id
    )

    if group is None:

        await message.answer(
            "🔫 Выбери группу, чтобы посмотреть",
            reply_markup=get_years_keyboard(),
        )

        return

    current_date = datetime.now().strftime(
        "%d.%m.%Y"
    )

    if not current_date:

        await message.answer(
            "🔦 Не вижу расписания, отдыхаем"
        )

        return

    lessons = get_lessons_by_date(
        group,
        current_date,
    )

    text = (
        f"📚 Расписание на {current_date}\n\n"
        f"🧭 Группа: {group}\n"
    )

    text += format_lessons(
        lessons
    )

    await message.answer(text)
