import asyncio
import logging
from aiogram import Bot, Dispatcher
import logging

from app.handlers import router

from app.database.models import create_table_days,create_time_table,create_user_table,create_childs_table,create_time_ch_tables,create_lesson_day_table,insert_into_days_table,insert_into_lesson_day
days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
clock = [
    ["12:30_Понедельник", "13:30_Понедельник"],
    ["12:30_Вторник", "13:30_Вторник"]
]
bot = Bot(token="8013109178:AAHGZ_if1VPNtsG2PmHG7KSZN5wo0NvtDlk")
dp = Dispatcher()
dp.include_router(router)

async def main():

    await create_childs_table()
    await create_lesson_day_table()
    await create_time_table(sum(clock, []))
    await create_table_days(days)
    await create_user_table()
    await create_time_ch_tables()
    await insert_into_days_table(sum(clock, []))
    await  insert_into_lesson_day(days)

    await dp.start_polling(bot)






if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)
    try:

        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
