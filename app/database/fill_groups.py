from app.database.database import SessionLocal
from app.database.models import Lesson
from app.database.group_model import Group


def fill_groups():

    db = SessionLocal()

    # очищаем старые записи
    db.query(Group).delete()

    # получаем все группы из lessons
    groups = (
        db.query(
            Lesson.group
        )
        .distinct()
        .all()
    )

    for (group_name,) in groups:

        try:

            year = group_name.split("-")[1]

        except Exception:

            continue

        db.add(
            Group(
                education_year=year,
                group_name=group_name
            )
        )

    db.commit()
    db.close()

    print("GROUPS FILLED")
