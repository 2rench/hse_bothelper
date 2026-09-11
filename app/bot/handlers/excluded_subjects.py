from aiogram import Router
from aiogram.types import (
    CallbackQuery,
)

from app.database.user_repository import (
    get_user,
    get_user_group,
    toggle_excluded_subject,
)

from app.services.schedule_service import (
    get_week_subjects,
)

router = Router()


PER_PAGE = 8


def get_excluded_subjects_keyboard(
    subjects: list[str],
    excluded: list[str],
    page: int = 0,
):

    from aiogram.types import (
        InlineKeyboardMarkup,
        InlineKeyboardButton,
    )

    total_pages = max(
        1,
        (
            len(subjects)
            + PER_PAGE
            - 1
        )
        // PER_PAGE,
    )

    if page < 0:
        page = 0

    if page >= total_pages:
        page = total_pages - 1

    start = (
        page
        * PER_PAGE
    )

    page_subjects = subjects[
        start:start + PER_PAGE
    ]

    buttons = []

    for index, subject in enumerate(
        page_subjects
    ):

        subject_index = (
            start
            + index
        )

        if subject in excluded:

            text = f"❌ {subject}"

        else:

            text = subject

        buttons.append(
            [
                InlineKeyboardButton(
                    text=text[:60],
                    callback_data=(
                        "excluded_subject:"
                        f"{subject_index}"
                    ),
                )
            ]
        )

    navigation = []

    if page > 0:

        navigation.append(
            InlineKeyboardButton(
                text="⬅️",
                callback_data=(
                    f"excluded_page:{page - 1}"
                ),
            )
        )

    navigation.append(
        InlineKeyboardButton(
            text=f"{page + 1}/{total_pages}",
            callback_data="excluded_page_current",
        )
    )

    if page + 1 < total_pages:

        navigation.append(
            InlineKeyboardButton(
                text="➡️",
                callback_data=(
                    f"excluded_page:{page + 1}"
                ),
            )
        )

    if total_pages > 1:

        buttons.append(
            navigation
        )

    return InlineKeyboardMarkup(
        inline_keyboard=buttons
    )


async def show_excluded_subjects(
    callback: CallbackQuery,
    page: int = 0,
):

    if callback.from_user is None:

        return

    telegram_id = (
        callback.from_user.id
    )

    group = get_user_group(
        telegram_id
    )

    if not group:

        await callback.answer(
            "Сначала выберите группу",
            show_alert=True,
        )

        return

    user = get_user(
        telegram_id
    )

    excluded = (
        user.get(
            "excluded_subjects",
            [],
        )
        if user
        else []
    )

    subjects = get_week_subjects(
        group
    )

    if not subjects:

        await callback.message.edit_text(
            "На текущей неделе "
            "предметов нет."
        )

        await callback.answer()

        return

    await callback.message.edit_text(
        "🚫 <b>Исключение пар</b>\n\n"
        "Нажмите на предмет, чтобы "
        "исключить или вернуть его:",
        reply_markup=(
            get_excluded_subjects_keyboard(
                subjects,
                excluded,
                page,
            )
        ),
    )

    await callback.answer()


@router.callback_query(
    lambda c:
    c.data == "excluded_subjects"
)
async def excluded_subjects_start(
    callback: CallbackQuery,
):

    await show_excluded_subjects(
        callback
    )


@router.callback_query(
    lambda c:
    c.data.startswith(
        "excluded_page:"
    )
)
async def excluded_subjects_page(
    callback: CallbackQuery,
):

    if callback.from_user is None:

        return

    page = int(
        callback.data.replace(
            "excluded_page:",
            "",
        )
    )

    telegram_id = (
        callback.from_user.id
    )

    group = get_user_group(
        telegram_id
    )

    if not group:

        await callback.answer(
            "Сначала выберите группу",
            show_alert=True,
        )

        return

    user = get_user(
        telegram_id
    )

    excluded = (
        user.get(
            "excluded_subjects",
            [],
        )
        if user
        else []
    )

    subjects = get_week_subjects(
        group
    )

    await callback.message.edit_reply_markup(
        reply_markup=(
            get_excluded_subjects_keyboard(
                subjects,
                excluded,
                page,
            )
        )
    )

    await callback.answer()


@router.callback_query(
    lambda c:
    c.data.startswith(
        "excluded_subject:"
    )
)
async def excluded_subject_toggle(
    callback: CallbackQuery,
):

    if callback.from_user is None:

        return

    telegram_id = (
        callback.from_user.id
    )

    group = get_user_group(
        telegram_id
    )

    if not group:

        await callback.answer(
            "Сначала выберите группу",
            show_alert=True,
        )

        return

    subject_index = int(
        callback.data.replace(
            "excluded_subject:",
            "",
        )
    )

    subjects = get_week_subjects(
        group
    )

    if (
        subject_index < 0
        or subject_index >= len(subjects)
    ):

        await callback.answer(
            "Предмет не найден",
            show_alert=True,
        )

        return

    subject = subjects[
        subject_index
    ]

    excluded = (
        toggle_excluded_subject(
            telegram_id,
            subject,
        )
    )

    user = get_user(
        telegram_id
    )

    if user is None:

        await callback.answer()

        return

    await callback.message.edit_reply_markup(
        reply_markup=(
            get_excluded_subjects_keyboard(
                subjects,
                excluded,
            )
        )
    )

    if subject in excluded:

        await callback.answer(
            f"❌ {subject}",
        )

    else:

        await callback.answer(
            f"✅ {subject}",
        )
