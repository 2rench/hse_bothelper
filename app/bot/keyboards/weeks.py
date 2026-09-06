from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


def get_weeks_keyboard(
    weeks: list[int],
    page: int = 0,
    per_page: int = 8,
) -> InlineKeyboardMarkup:

    start = page * per_page
    end = start + per_page

    page_weeks = weeks[
        start:end
    ]

    buttons = []

    for week in page_weeks:

        buttons.append(
            [
                InlineKeyboardButton(
                    text=f"🗓 Неделя №{week}",
                    callback_data=f"select_week:{week}",
                )
            ]
        )

    navigation = []

    total_pages = (
        (len(weeks) + per_page - 1)
        // per_page
    )

    if page > 0:

        navigation.append(
            InlineKeyboardButton(
                text="⬅️",
                callback_data=f"weeks_page:{page - 1}",
            )
        )

    navigation.append(
        InlineKeyboardButton(
            text=f"{page + 1}/{total_pages}",
            callback_data="weeks_page_current",
        )
    )

    if page + 1 < total_pages:

        navigation.append(
            InlineKeyboardButton(
                text="➡️",
                callback_data=f"weeks_page:{page + 1}",
            )
        )

    if total_pages > 1:

        buttons.append(
            navigation
        )

    return InlineKeyboardMarkup(
        inline_keyboard=buttons
    )
