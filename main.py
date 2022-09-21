import asyncio
import datetime
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

import bootstrap
import router
import services
from config import config
from services import horoscope_mailing


async def main():
    bootstrap.bootstrap()

    db = bootstrap.Database().getInstance()
    db.casino.support_queue.delete_many({})

    bot = bootstrap.MyBot().getInstance()
    dp = bootstrap.MyDispatcher().getInstance()

    scheduler = AsyncIOScheduler()
    scheduler.add_job(horoscope_mailing.mail_all_subscribers, IntervalTrigger(days=1, start_date=datetime.datetime.now().replace(hour=6, minute=0, second=0)))

    router.register_commands()

    await services.register_default_commands()

    for admin_id in config('admins'):
        await bot.send_message(admin_id, "<b>Бот запущен</b>")

    scheduler.start()
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
