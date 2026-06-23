from datetime import datetime

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.services.schedule_service import (
    get_lessons_by_date,
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

from app.database.user_repository import (
    increase_command,
)
from app.bot.services.formatter import (
    format_lessons,
    get_today_no_lessons,
)

router = Router()


@router.message(Command("today"))
async def today_handler(
    message: Message,
):
    increase_command('today')
    group = get_user_group(
        message.from_user.id
    )

    if group is None:

        await message.answer(
            "🔫 Выбери группу, чтобы посмотреть расписание",
            reply_markup=get_years_keyboard(),
        )

        return

    current_date = datetime.now().strftime(
        "%d.%m.%Y"
    )

    lessons = get_lessons_by_date(
        group,
        current_date,
    )

    if not lessons:

        await message.answer(
            f"{get_today_no_lessons(message.from_user.id)} "
        )

        return

    text = (
        "📚 Расписание на сегодня\n"
    )

    text += format_lessons(
        lessons,
        telegram_id=message.from_user.id,
    )

    await message.answer(
        text
    )


@router.message(
    lambda m: m.text == "📅 Сегодня"
)
async def today_button(
    message: Message,
):
    await today_handler(
        message
    )
