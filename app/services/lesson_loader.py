from app.database.database import SessionLocal
from app.database.models import Lesson
from app.services.schedule_name_normalizer import (
    normalize_schedule_name,
)


def load_lessons(
    lessons_data: list[dict],
):
    """
    Загружает lessons в SQLite.
    """

    db = SessionLocal()

    objects = []

    for item in lessons_data:

        lesson = Lesson(
            group_name=item["group"],
            day=item["day"],
            date=item["date"],
            lesson_number=item["lesson_number"],
            lesson_time=item["lesson_time"],
            subject=item["subject"],
            teacher=item["teacher"],
            room=item["room"],
            building=item["building"],
            is_online=item.get(
                "is_online",
                False,
            ),
            lesson_type=item.get(
                "lesson_type"
            ),
            schedule_name=normalize_schedule_name(
                item.get("schedule_name")
            ),
            schedule_type=item.get(
                "schedule_type"
            ),
        )

        objects.append(
            lesson
        )

    db.bulk_save_objects(
        objects
    )

    db.commit()
    db.close()
