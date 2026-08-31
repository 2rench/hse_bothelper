from collections import defaultdict

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.services.schedule_service import (
    get_week_lessons,
)

from app.database.user_repository import (
    get_user_group,
    increase_command,
)

from app.bot.keyboards.group_years import (
    get_years_keyboard,
)

from app.bot.services.formatter import (
    format_lessons,
    get_week_no_lessons,
)

router = Router()


@router.message(Command("week"))
async def week_handler(
    message: Message,
):

    if message.from_user is None:
        return

    if message.bot is None:
        return

    telegram_id = message.from_user.id
    bot = message.bot

    increase_command(
        "week"
    )

    group = get_user_group(
        telegram_id
    )

    if group is None:

        await message.answer(
            "Выбери группу",
            reply_markup=get_years_keyboard(),
        )

        return

    lessons = get_week_lessons(
        group
    )

    if not lessons:

        try:

            await bot.unpin_all_chat_messages(
                message.chat.id
            )

        except Exception:
            pass

        await message.answer(
            get_week_no_lessons(
                telegram_id
            )
        )

        return

    grouped = defaultdict(list)

    for lesson in lessons:

        grouped[
            (
                lesson.day,
                lesson.date,
            )
        ].append(
            lesson
        )

    sent_messages = []

    for (
        day,
        date,
    ), day_lessons in grouped.items():

        text = (
            f"━━━━━━━━━━━━\n"
            f"📚 <b>{day} — {date}</b>\n"
            f"🧭 Группа: {group}\n"
            f"━━━━━━━━━━━━\n\n"
        )

        text += format_lessons(
            day_lessons,
            telegram_id=telegram_id,
        )

        msg = await message.answer(
            text
        )

        sent_messages.append(
            msg
        )

    try:

        await bot.unpin_all_chat_messages(
            message.chat.id
        )

    except Exception:
        pass

    try:

        await bot.pin_chat_message(
            chat_id=message.chat.id,
            message_id=sent_messages[-1].message_id,
        )

    except Exception:
        pass


@router.message(
    lambda m: m.text == "🗓 Неделя"
)
async def week_button(
    message: Message,
):

    await week_handler(
        message
    )
