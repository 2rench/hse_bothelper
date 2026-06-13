from datetime import datetime, timedelta

from aiogram import Bot

from app.database.user_repository import (
    get_users_for_tomorrow_notifications,
)

from app.services.schedule_service import (
    get_lessons_by_date,
)

from app.database.session_repository import (
    get_session_lessons,
)


_last_sent_date = None


async def send_tomorrow_notifications(
    bot: Bot,
):

    global _last_sent_date

    now = datetime.now()

    today_key = now.strftime(
        "%d.%m.%Y"
    )

    if _last_sent_date == today_key:
        return

    # 20:00
    if now.hour < 20:
        return

    tomorrow = (
        now + timedelta(days=1)
    ).strftime("%d.%m.%Y")

    users = (
        get_users_for_tomorrow_notifications()
    )

    for user in users:

        lessons = get_lessons_by_date(
            user.group_name,
            tomorrow,
        )

        if not lessons:
            continue

        first = lessons[0]

        is_session = (
            first.schedule_name
            and
            "СЕССИЯ"
            in first.schedule_name.upper()
        )

        if is_session:

            text = (
                "🎓 Напоминание\n\n"
                f"Завтра сессия\n"
                f"{tomorrow}"
            )

        else:

            text = (
                "📚 Напоминание\n\n"
                f"Завтра пары\n"
                f"{tomorrow}\n"
                f"Количество: {len(lessons)}"
            )

        try:

            await bot.send_message(
                user.telegram_id,
                text,
            )

        except Exception as e:

            print(
                "TOMORROW ERROR:",
                e,
            )

    _last_sent_date = today_key
