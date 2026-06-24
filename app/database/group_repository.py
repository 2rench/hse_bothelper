from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.database.group_model import Group


def save_group(
    group_name: str,
):

    db: Session = SessionLocal()

    try:

        year = group_name.split("-")[1]

        exists = (
            db.query(Group)
            .filter(
                Group.group_name == group_name
            )
            .first()
        )

        if not exists:

            group = Group(
                education_year=year,
                group_name=group_name,
            )

            db.add(group)

            db.commit()

    finally:

        db.close()


def get_groups_by_year(
    year: str,
):

    db: Session = SessionLocal()

    groups = (
        db.query(Group)
        .filter(
            Group.education_year == year
        )
        .order_by(
            Group.group_name
        )
        .all()
    )

    db.close()

    return [
        group.group_name
        for group in groups
    ]


def get_all_groups():

    db = SessionLocal()

    groups = (
        db.query(Group)
        .order_by(
            Group.group_name
        )
        .all()
    )

    db.close()

    return groups


def clear_groups():

    db = SessionLocal()

    db.query(Group).delete()

    db.commit()

    db.close()
