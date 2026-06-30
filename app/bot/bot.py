import asyncio
import os


from aiogram import Bot, Dispatcher

from aiogram.client.default import (
    DefaultBotProperties,
)

from aiogram.enums import ParseMode

from dotenv import load_dotenv

from app.bot.handlers.group_select import router as group_router
from app.bot.handlers.help import router as help_router
from app.services.scheduler import (
    schedule_loop,
)
from app.bot.handlers.unknown import router as unknown_router
from app.bot.handlers.sport_schedule import router as sport_router
from app.admin.admin_router import (
    router as admin_router
)
from app.bot.handlers import start, today, week, tomorrow, sessions
from app.bot.handlers.notifications import (
    router as notifications_router
)
from app.bot.handlers.themes import (
    router as themes_router,
)

from app.database.database import (
    Base,
    engine,
)

from app.bot.handlers.open_notification_day import (
    router as open_day_router
)

from app.bot.handlers.open_notification_schedule import (
    router as notification_open_router
)

from app.bot.handlers.home import (
    router as home_router
)

from app.bot.handlers.session_view import router as session_view_router
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def main():

    Base.metadata.create_all(engine)

    bot = Bot(
        token=BOT_TOKEN,

        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
        ),
    )

    await bot.delete_webhook(
        drop_pending_updates=True
    )
    dp = Dispatcher()

    dp.include_router(group_router)
    dp.include_router(tomorrow.router)
    dp.include_router(start.router)
    dp.include_router(today.router)
    dp.include_router(week.router)
    dp.include_router(sessions.router)
    dp.include_router(session_view_router)
    dp.include_router(notifications_router)
    dp.include_router(notification_open_router)
    dp.include_router(open_day_router)
    dp.include_router(home_router)
    dp.include_router(help_router)
    dp.include_router(admin_router)
    dp.include_router(sport_router)
    dp.include_router(themes_router)
    dp.include_router(unknown_router)

    asyncio.create_task(
        schedule_loop(bot)
    )

    await dp.start_polling(bot)

if __name__ == '__main__':

    asyncio.run(main())
