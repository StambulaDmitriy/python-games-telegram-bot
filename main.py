import asyncio

import bootstrap
import router
import services
from config import config


async def main():
    bootstrap.bootstrap()

    bot = bootstrap.MyBot().getInstance()
    dp = bootstrap.MyDispatcher().getInstance()

    router.register_commands()

    await services.register_default_commands()

    for admin_id in config('admins'):
        await bot.send_message(admin_id, "<b>Бот запущен</b>")

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
