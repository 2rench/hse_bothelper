from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.database.user_model import User

from app.database.command_stat_model import (
    CommandStat,
)


def save_user_group(
    telegram_id: int,
    group_name: str,
):

    db: Session = SessionLocal()

    user = (
        db.query(User)
        .filter(
            User.telegram_id == telegram_id
        )
        .first()
    )

    if user:

        user.group_name = group_name

    else:

        user = User(
            telegram_id=telegram_id,
            group_name=group_name,
            schedule_updates=True,
            tomorrow_notifications=False,
        )

        db.add(user)

    db.commit()

    db.close()


def get_user_group(
    telegram_id: int,
) -> str | None:

    db: Session = SessionLocal()

    user = (
        db.query(User)
        .filter(
            User.telegram_id == telegram_id
        )
        .first()
    )

    db.close()

    if not user:
        return None

    return user.group_name

def get_user(
    telegram_id: int,
):

    db: Session = SessionLocal()

    user = (
        db.query(User)
        .filter(
            User.telegram_id == telegram_id
        )
        .first()
    )

    if not user:

        db.close()

        return None

    data = {
        "telegram_id": user.telegram_id,
        "group_name": user.group_name,
        "schedule_updates": user.schedule_updates,
        "tomorrow_notifications": user.tomorrow_notifications,
    }

    db.close()

    return data

def toggle_schedule_updates(
    telegram_id: int,
):

    db: Session = SessionLocal()

    user = (
        db.query(User)
        .filter(
            User.telegram_id == telegram_id
        )
        .first()
    )

    if user:

        user.schedule_updates = (
            not user.schedule_updates
        )

        db.commit()

    db.close()

def toggle_tomorrow_notifications(
    telegram_id: int,
):

    db: Session = SessionLocal()

    user = (
        db.query(User)
        .filter(
            User.telegram_id == telegram_id
        )
        .first()
    )

    if user:

        user.tomorrow_notifications = (
            not user.tomorrow_notifications
        )

        db.commit()

    db.close()

def get_users_for_schedule_updates():

    db: Session = SessionLocal()

    users = (
        db.query(User)
        .filter(
            User.schedule_updates == True
        )
        .all()
    )

    db.close()

    return users

def get_users_for_tomorrow_notifications():

    db: Session = SessionLocal()

    users = (
        db.query(User)
        .filter(
            User.tomorrow_notifications == True
        )
        .all()
    )

    db.close()

    return users

def get_all_users():

    db = SessionLocal()

    users = db.query(User).all()

    db.close()

    return users


def increase_command(
    command_name: str,
):

    db = SessionLocal()

    stat = (
        db.query(CommandStat)
        .filter(
            CommandStat.command_name
            == command_name
        )
        .first()
    )

    if stat:

        stat.count += 1

    else:

        db.add(
            CommandStat(
                command_name=command_name,
                count=1,
            )
        )

    db.commit()
    db.close()


def get_command_stats():

    db = SessionLocal()

    stats = db.query(
        CommandStat
    ).all()

    db.close()

    return stats