from typing import Type
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import BaseORM


class BaseRepository:
    model: Type[BaseORM] | None = None

    def __init__(self, session: AsyncSession) -> None:
        self.session: AsyncSession = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)  # type: ignore
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)  # type: ignore
        result = await self.session.execute(query)
        return result.scalars().all()
