from sqlalchemy import select, insert, func

from repositories.base import BaseRepository
from src.models.hotels import HotelsOrm

from src.database import engine


class HotelsRepository(BaseRepository):
    model = HotelsOrm

    async def get_all(self, location, title, limit, offset):
        query = select(HotelsOrm)
        if title:
            query = query.filter(
                func.lower(HotelsOrm.title).contains(title.strip().lower())
            )
        if location:
            query = query.filter(
                func.lower(HotelsOrm.locations).contains(location.strip().lower())
            )
        query = query.limit(limit).offset(offset)  # type: ignore

        print(query.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)
        hotels = result.scalars().all()
        return hotels
