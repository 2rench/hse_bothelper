import asyncio

from app.services.check_schedule_updates import (
    check_updates,
)

from app.services.notification_service import (
    send_update_notifications,
)

from app.services.tomorrow_notifications import (
    send_tomorrow_notifications,
)


last_backup_hour = None
last_cleanup_day = None


async def schedule_loop(
    bot,
):

    global last_backup_hour
    global last_cleanup_day

    while True:

        try:

            print(
                "CHECKING UPDATES..."
            )

            updates = check_updates()

            await send_update_notifications(
                bot,
                updates,
            )

            await send_tomorrow_notifications(
                bot,
            )

            print(
                "CHECK FINISHED"
            )

        except Exception as error:

            print(
                "SCHEDULER ERROR:",
                error,
            )

        await asyncio.sleep(
            1800
        )
