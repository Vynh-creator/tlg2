from sqlalchemy import BigInteger, String, ForeignKey,MetaData,TIME
from sqlalchemy.log import echo_property
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
engine = create_async_engine(url="postgresql+asyncpg://postgres:456rty@localhost/tlg",echo=True)
async_session = async_sessionmaker(engine)
metadata=MetaData()

class Base(AsyncAttrs, DeclarativeBase):
    pass







async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
