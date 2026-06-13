from app.database.user_repository import (
    get_users_for_schedule_updates,
)

from app.bot.keyboards.update_notification import (
    get_update_keyboard,
)

from app.database.sent_notification_repository import (
    was_sent,
    mark_sent,
)

async def send_update_notifications(
    bot,
    updates,
):

    if not updates:
        return

    users = (
        get_users_for_schedule_updates()
    )

    for user in users:

        for update in updates:

            if update["type"] == "new":

                text = (
                    "📢 Новое расписание\n\n"
                    f"{update['name']}"
                )

            else:

                text = (
                    "✏️ Расписание обновлено\n\n"
                    f"{update['name']}"
                )

            try:

                await bot.send_message(
                    chat_id=user.telegram_id,
                    text=text,
                    reply_markup=get_update_keyboard(
                        update["week"],
                        update["is_session"],
                    ),
                )

            except Exception as e:

                print(
                    "NOTIFICATION ERROR:",
                    e,
                )
