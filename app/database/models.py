from sqlalchemy import BigInteger, String, ForeignKey,MetaData,TIME
from sqlalchemy.log import echo_property
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.sql.coercions import expect

engine = create_async_engine(url="postgresql+asyncpg://postgres:456rty@localhost/tlg",echo=True)
async_session = async_sessionmaker(engine)
metadata=MetaData()
from sqlalchemy.exc import SQLAlchemyError

# days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]

class Base(AsyncAttrs, DeclarativeBase):
    pass


async def create_user_table():
    async with async_session() as session:
        await session.execute("""
        CREATE TABLE IF NOT EXISTS public.user_inf
(
    user_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    tg_id bigint,
    first_name_p character varying(20) COLLATE pg_catalog."default",
    last_name_p character varying(20) COLLATE pg_catalog."default",
    phone character varying(20) COLLATE pg_catalog."default",
    chat_id bigint,
    CONSTRAINT pk_book_book_id PRIMARY KEY (user_id)
)
        """)
        await session.commit()



async def create_lesson_day_table():
    async with async_session() as session:
        await session.execute("""
        CREATE TABLE IF NOT EXISTS public.lesson_day
(
    day_id character varying(20) COLLATE pg_catalog."default" NOT NULL,
    state_fill boolean NOT NULL DEFAULT false,
    CONSTRAINT lesson_day_pkey PRIMARY KEY (day_id)
)
        """)
        await session.commit()






async def insert_into_lesson_day(days: list[str]):
    async with async_session() as session:
        async with session.begin():
            try:
                for day in days:
                    await session.execute("""
                    INSERT INTO lesson_day (day_id)
                    VALUES (:day_id)
                    """, {'day_id': day})

                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                print(f"Error occurred: {e}")

async def create_table_days(days: list[str]):
    async with async_session() as session:
        async with session.begin():
            try:

               for day in days:
                   table_name=f"public.{day}"
                   await session.execute(f"""
                CREATE TABLE IF NOT EXISTS {table_name}
(
    state_fill boolean DEFAULT false,
    time_less character varying(20) COLLATE pg_catalog."default",
    time_id serial PRIMARY KEY,

)

                """)
                   await session.commit()
            except Exception as e:
                await session.rollback()
                print(f'Error occured: {e}')


async def create_time_ch_tables():
    async with async_session() as session:
        async with session.begin():
            await session.execute(""" 
            CREATE TABLE IF NOT EXISTS public.time_ch
(
    time_ch_id integer NOT NULL DEFAULT nextval('time_ch_time_ch_id_seq'::regclass),
    day_name character varying(20) COLLATE pg_catalog."default",
    "time" character varying(30) COLLATE pg_catalog."default",
    child_id integer
)
            """)
            await session.commit()


async def insert_into_days_table(times: list[str]):
    async with async_session() as session:
        async with session.begin():
            try:
               for time in times:
                   table_name=f'public.{time.split('_')[1]}'
                   await session.execute(f""" 
                   INSERT INTO {table_name} (time_less)
                   VALUES (:time)
                   """,{'time':time})
                   await session.commit()
            except Exception as e:
                await session.rollback()
                print(f'Exception occured {e}')


async def create_time_table(times: list[list[str]]):
    async with async_session() as session:
        async with session.begin():
            try:
               for time in times:
                   table_name=f'public.{time}'
                   await session.execute(f""" 
   CREATE TABLE IF NOT EXISTS {table_name}
(
    id_pers NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 12 CACHE 1 ),
    tg_id bigint,
    child_id integer,
    CONSTRAINT fk_id_pers_id_pers FOREIGN KEY (child_id)

)""")

                   await session.commit()
            except Exception as e:
                await session.rollback()
                print(f'Exception occured {e}')

async def create_childs_table():
    async with async_session() as session:
        async with session.begin():
            try:
                session.execute("""
                CREATE TABLE IF NOT EXISTS public.childs
(
    child_id integer NOT NULL DEFAULT nextval('childs_child_id_seq'::regclass),
    first_name character varying(20) COLLATE pg_catalog."default",
    last_name character varying(20) COLLATE pg_catalog."default",
    user_id integer,
    miss_less integer DEFAULT 0,
    CONSTRAINT childs_pkey PRIMARY KEY (child_id),
    CONSTRAINT fk_user_id_user_id FOREIGN KEY (user_id)
        REFERENCES public.user_inf (user_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

                """)
            except Exception as e:
                await session.rollback()
                print(f'Exception occured {e}')






async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
