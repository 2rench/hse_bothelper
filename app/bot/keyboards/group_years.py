from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.database import SessionLocal
from app.database.models import Lesson


def get_years_keyboard() -> InlineKeyboardMarkup:
    """
    Клавиатура выбора года поступления.
    """

    db = SessionLocal()

    groups = (
        db.query(Lesson.group_name)
        .distinct()
        .all()
    )

    db.close()

    years = set()

    for group_tuple in groups:

        group_name = group_tuple[0]

        try:
            year = group_name.split("-")[1]
            years.add(year)
        except Exception:
            continue

    years = sorted(years, reverse=True)

    builder = InlineKeyboardBuilder()

    for year in years:
        builder.button(
            text=f"20{year}",
            callback_data=f"year:{year}",
        )

    builder.adjust(2)

    return builder.as_markup()