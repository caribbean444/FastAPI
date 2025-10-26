from typing import Type
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import BaseORM

from src.database import engine

from pydantic import BaseModel


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

    async def add(self, data: BaseModel):
        add_data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)  # type: ignore
        print(
            add_data_stmt.compile(engine, compile_kwargs={"literal_binds": True})
        )  # * Вывод сырого SQL запроса
        result = await self.session.execute(add_data_stmt)
        return result.scalars().one()
