import asyncio
import logging
from aiogram import Bot, Dispatcher
import logging

from app.handlers import router

from app.database.models import async_main,create_table_days,create_time_table,create_user_table,create_childs_table,create_time_ch_tables,create_lesson_day_table,insert_into_days_table,insert_into_lesson_day



async def main():
    await async_main()
    bot = Bot(token="8013109178:AAHGZ_if1VPNtsG2PmHG7KSZN5wo0NvtDlk")
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(create_childs_table())
        asyncio.run(create_lesson_day_table())
        asyncio.run(create_time_table())
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
