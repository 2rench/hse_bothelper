import asyncio
from pathlib import Path

from aiogram.types import FSInputFile

from app.database.user_repository import (
    get_all_users,
)


async def send_broadcast(
    bot,
    text: str,
    image_path: str | None,
):

    users = get_all_users()

    success = 0
    failed = 0

    for user in users:

        try:

            if image_path:

                await bot.send_photo(
                    chat_id=user.telegram_id,
                    photo=FSInputFile(
                        image_path
                    ),
                    caption=text
                )

            else:

                await bot.send_message(
                    user.telegram_id,
                    text
                )

            success += 1

        except Exception:

            failed += 1

        await asyncio.sleep(
            0.05
        )

    if image_path:

        Path(image_path).unlink(
            missing_ok=True
        )

    return success, failed
