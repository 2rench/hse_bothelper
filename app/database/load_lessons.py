import json

from pathlib import Path

from app.database.database import SessionLocal
from app.database.models import Lesson

JSON_PATH = Path("files/parsed_schedule.json")

def load_lessons():

    if not JSON_PATH.exists():

        raise FileNotFoundError(
            f"JSON not found: {JSON_PATH}"
        )

    with open(
        JSON_PATH,
        "r",
        encoding="utf-8",
    ) as file:

        lessons_data = json.load(file)

    db = SessionLocal()

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

            lesson_type=item.get("lesson_type"),
        )

        db.add(lesson)

    db.commit()

    db.close()

    print(
        f"Loaded {len(lessons_data)} lessons"
    )

if __name__ == '__main__':

    load_lessons()
