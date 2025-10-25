from typing import Type
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import BaseORM

from src.database import engine


class BaseRepository:
    model: Type[BaseORM] | None = None

    def __init__(self, session: AsyncSession) -> None:
        self.session: AsyncSession = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)  # type: ignore
        print(query.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)  # type: ignore
        result = await self.session.execute(query)
        return result.scalars().all()

    async def add(self, *args, **kwargs):
        add_hotel_stmt = insert(self.model).values(**kwargs)  # type: ignore
        print(
            add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True})
        )  # * Вывод сырого SQL запроса
        return await self.session.execute(add_hotel_stmt)
