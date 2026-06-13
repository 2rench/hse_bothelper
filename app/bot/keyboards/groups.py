from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.database import SessionLocal
from app.database.models import Lesson


def get_groups_keyboard(year: str) -> InlineKeyboardMarkup:
    """
    Клавиатура групп по году.
    """

    db = SessionLocal()

    groups = (
        db.query(Lesson.group_name)
        .distinct()
        .all()
    )

    db.close()

    filtered_groups = []

    for group_tuple in groups:

        group_name = group_tuple[0]

        if f"-{year}-" in group_name:
            filtered_groups.append(group_name)

    filtered_groups = sorted(filtered_groups)

    builder = InlineKeyboardBuilder()

    for group in filtered_groups:

        builder.button(
            text=group,
            callback_data=f"group:{group}",
        )

    builder.adjust(2)

    return builder.as_markup()