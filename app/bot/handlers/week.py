from collections import defaultdict

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import (
    Message,
    CallbackQuery,
)

from app.services.schedule_service import (
    get_week_lessons,
    get_week_lessons_by_number,
    get_available_week_numbers,
    get_current_schedule_week,
)

from app.database.user_repository import (
    get_user_group,
    increase_command,
)

from app.bot.keyboards.group_years import (
    get_years_keyboard,
)

from app.bot.keyboards.weeks import (
    get_weeks_keyboard,
)

from app.bot.services.formatter import (
    format_lessons,
    get_week_no_lessons,
)

router = Router()


async def send_selected_week(
    message,
    group: str,
    week: int,
    telegram_id: int,
    pin_message: bool = False,
):

    lessons = get_week_lessons_by_number(
        group,
        week,
    )

    if not lessons:

        await message.answer(
            "Расписание не найдено"
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
            f"<b>{day} — {date}</b>\n\n"
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

    if not pin_message:

        return

    if not sent_messages:

        return

    try:

        await message.bot.unpin_all_chat_messages(
            message.chat.id
        )

    except Exception:

        pass

    try:

        await message.bot.pin_chat_message(
            chat_id=message.chat.id,
            message_id=(
                sent_messages[-1].message_id
            ),
        )

    except Exception:

        pass


@router.message(Command("week"))
async def week_handler(
    message: Message,
):

    if message.from_user is None:

        return

    if message.bot is None:

        return

    telegram_id = message.from_user.id

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

    weeks = get_available_week_numbers(
        group
    )

    # Если доступна только одна неделя,
    # сразу показываем её как раньше.

    if len(weeks) <= 1:

        current_week = (
            weeks[0]
            if weeks
            else None
        )

        if current_week is None:

            try:

                await message.bot.unpin_all_chat_messages(
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

        current_schedule_week = (
            get_current_schedule_week(
                group
            )
        )

        await send_selected_week(
            message,
            group,
            current_week,
            telegram_id,
            pin_message=(
                current_week
                == current_schedule_week
            ),
        )

        return

    # Если недель несколько —
    # показываем меню выбора.

    await message.answer(
        "📚 <b>Выберите неделю:</b>",
        reply_markup=get_weeks_keyboard(
            weeks
        ),
    )


@router.callback_query(
    lambda c:
    c.data.startswith(
        "select_week:"
    )
)
async def select_week(
    callback: CallbackQuery,
):

    if callback.from_user is None:

        return

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
            "select_week:",
            "",
        )
    )

    current_week = get_current_schedule_week(
        group
    )

    await callback.message.delete()

    await send_selected_week(
        callback.message,
        group,
        week,
        callback.from_user.id,
        pin_message=(
            week == current_week
        ),
    )

    await callback.answer()


@router.callback_query(
    lambda c:
    c.data.startswith(
        "weeks_page:"
    )
)
async def weeks_page(
    callback: CallbackQuery,
):

    if callback.from_user is None:

        return

    group = get_user_group(
        callback.from_user.id
    )

    if not group:

        await callback.answer(
            "Сначала выберите группу",
            show_alert=True,
        )

        return

    page = int(
        callback.data.replace(
            "weeks_page:",
            "",
        )
    )

    weeks = get_available_week_numbers(
        group
    )

    await callback.message.edit_reply_markup(
        reply_markup=get_weeks_keyboard(
            weeks,
            page=page,
        )
    )

    await callback.answer()


@router.message(
    lambda m:
    m.text == "🗓 Неделя"
)
async def week_button(
    message: Message,
):

    await week_handler(
        message
    )
