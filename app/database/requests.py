from sqlalchemy import select, table,MetaData
from sqlalchemy.orm import Mapped

import app.database.models as md
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.exc import IntegrityError


# async def set_user(tg_id):
#     async with md.async_session() as session:
#         user = await session.scalar(select(md.User).where(md.User.tg_id == tg_id))
#         if not user:
#             session.add(md.User(tg_id=tg_id))
#             await session.commit()
from sqlalchemy.exc import SQLAlchemyError

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text

async def check_time(time_name, day_name):
    async with md.async_session() as session:
        try:

            await check_persons(time_name, day_name)


            result = await session.execute(text(f"SELECT COUNT(*) FROM {day_name} WHERE state_fill = TRUE"))
            count_true = result.scalar()


            total_count_result = await session.execute(text(f"SELECT COUNT(*) FROM {day_name}"))
            total_count = total_count_result.scalar()


            state_fill = True if count_true == total_count else False



            await session.execute(
                text(
                    """INSERT INTO lesson_day (day_id, state_fill)
                       VALUES (:day_name, :state_fill)
                       ON CONFLICT (day_id) DO UPDATE 
                       SET state_fill = EXCLUDED.state_fill"""
                ),
                {'state_fill': state_fill,
                 'day_name': day_name}
            )




            status = "full" if state_fill == 1 else "not full"
            print(f"Day {day_name} is {status}")


            await session.commit()

        except SQLAlchemyError as e:
            print(f"An error occurred: {e}")
            await session.rollback()





async def check_persons(time_name, day_name):
    async with md.async_session() as session:
        try:

            result = await session.execute(text(f"""SELECT MAX(id_pers) FROM {time_name}"""))
            max_id_pers = result.scalar() or 0


            state_fill = False if max_id_pers < 12 else True


            await session.execute(
                text(f"INSERT INTO {day_name} (state_fill) VALUES (:state_fill)"),
                {'state_fill': state_fill}
            )


            status = "not full" if state_fill == 0 else "full"
            print(f"time {time_name} is {status}")


            await session.commit()

        except SQLAlchemyError as e:
            print(f"An error occurred: {e}")
            await session.rollback()




async def get_days():
    async with md.async_session() as session:
        result = await session.execute(text("SELECT day_id FROM lesson_day WHERE state_fill = False"))
        return result.scalars().all()


async def get_time(tablename):
    async with md.async_session() as session:
        result= await session.execute((text(f"SELECT time_less FROM {tablename} WHERE state_fill=False")))
        return result.scalars().all()

async def registration(tg_id, first_name_p, last_name_p, phone, chat_id, first_name, last_name, day_name, time):
            async with md.async_session() as session:
                try:
                    query = text("""
                        INSERT INTO user_inf (tg_id, first_name_p, last_name_p, phone, chat_id) 
                        VALUES (:tg_id, :first_name_p, :last_name_p, :phone, :chat_id)
                    """)

                    await session.execute(query, {
                        'tg_id': tg_id,
                        'first_name_p': first_name_p,
                        'last_name_p': last_name_p,
                        'phone': phone,
                        'chat_id': chat_id
                    })

                    result = await session.execute(text("SELECT user_id FROM user_inf WHERE tg_id = :tg_id"),
                                                   {'tg_id': tg_id})
                    user_row = result.fetchone()

                    if user_row is None:
                        raise ValueError("User not found after insertion.")

                    user_id = user_row[0]

                    query = text("""INSERT INTO childs (first_name, last_name, user_id)
                                    VALUES (:first_name, :last_name, :user_id)""")
                    await session.execute(query, {
                        "first_name": first_name,
                        "last_name": last_name,
                        "user_id": user_id
                    })

                    result = await session.execute(text("SELECT child_id FROM childs WHERE user_id = :user_id"),
                                                   {'user_id': user_id})
                    child_id_row = result.fetchone()
                    if child_id_row is None:
                        raise ValueError("User not found after insertion.")
                    child_id = child_id_row[0]

                    query = text("""INSERT INTO time_ch (day_name, time, child_id)
                                    VALUES (:day_name, :time, :child_id)""")
                    await session.execute(query, {
                        "day_name": day_name,
                        "time": time,
                        "child_id": child_id
                    })


                    await check_time(time, day_name)

                    allowed_tables = ['12:30_Понедельник']
                    if time not in allowed_tables:
                        raise ValueError("Invalid table name")

                    query = text(f"""INSERT INTO {time} (child_id) VALUES (:child_id)""")
                    await session.execute(query, {"child_id": child_id})

                    await check_time(time, day_name)

                except Exception as e:
                    print(f"An error occurred: {e}")
                await session.commit()





# async def get_time( nameday: str):
#     # Динамическое создание таблицы
#     async with md.async_session() as session:
#       table_obj = table(nameday, md.metadata, autoload_with=md.engine)
#
#     # Запрос для получения данных
#       stmt = select(table_obj.c.time).where(table_obj.c.time != True)
#
#     # Выполнение запроса
#       result = await session.scalars(stmt)

#      return result.all()  # Возвращаем все результаты

