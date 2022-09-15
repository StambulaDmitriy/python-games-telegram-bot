import asyncio

from aiogram import Bot, Dispatcher

from config import config


async def main():
    bot = Bot(token=config('token'), parse_mode="HTML")
    dp = Dispatcher()

    for admin_id in config('admins'):
        await bot.send_message(admin_id, "<b>Бот запущен</b>")

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
