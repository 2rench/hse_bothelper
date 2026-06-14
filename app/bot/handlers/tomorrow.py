from datetime import (
    datetime,
    timedelta,
)

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.database.user_repository import (
    get_user_group,
)

from app.bot.keyboards.group_years import (
    get_years_keyboard,
)

from app.bot.services.formatter import (
    format_lessons,
)

from app.services.schedule_service import (
    get_lessons_by_date,
)

router = Router()


@router.message(
    Command("tomorrow")
)
async def tomorrow_handler(
    message: Message,
):

    group = get_user_group(
        message.from_user.id
    )

    if group is None:

        await message.answer(
            "🔫 Выбери группу, чтобы посмотреть",
            reply_markup=get_years_keyboard(),
        )

        return

    tomorrow_date = (
        datetime.now()
        + timedelta(days=1)
    ).strftime(
        "%d.%m.%Y"
    )

    lessons = get_lessons_by_date(
        group,
        tomorrow_date,
    )

    if not lessons:

        await message.answer(
            f"Завтра ({tomorrow_date}) без пар 🙏🙏🙏"
        )

        return

    text = (
        f"👀 На завтра — {tomorrow_date}\n\n"
    )

    text += format_lessons(
        lessons
    )

    await message.answer(
        text
    )
