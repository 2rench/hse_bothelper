import asyncio
from datetime import datetime

from app.services.check_schedule_updates import (
    check_updates,
)

from app.services.notification_service import (
    send_update_notifications,
)

from app.services.tomorrow_notifications import (
    send_tomorrow_notifications,
)

from app.database.backup_service import (
    backup_and_upload,
)

from app.database.cleanup_backups import (
    cleanup_backups,
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

            now = datetime.now()

            # Бэкап раз в час
            if last_backup_hour != now.hour:

                backup_and_upload()

                last_backup_hour = now.hour

            # Очистка в 12:00 один раз в сутки
            if (
                now.hour == 12
                and last_cleanup_day != now.date()
            ):

                cleanup_backups()

                last_cleanup_day = now.date()

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
