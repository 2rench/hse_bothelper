from pathlib import Path

from aiogram import Router, F
from aiogram.types import Message

router = Router()


@router.message(lambda m: m.text == "🏃 Физ–ра")
async def sport_schedule(
        message: Message,
):

    folder = Path(
        "files/schedule"
    )

    images = sorted(
        folder.glob("*.jpeg")
    )

    if not images:

        await message.answer(
            "😔 Расписание пока не загружено"
        )
        return

    media = []

    from aiogram.types import (
        FSInputFile,
    )

    for image in images:

        media.append(
            FSInputFile(
                image
            )
        )

    for image in media:

        await message.answer_photo(
            image
        )
