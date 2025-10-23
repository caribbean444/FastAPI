from fastapi import Body, APIRouter, Query
from pydantic import BaseModel, Field

from sqlalchemy import insert, select

from src.api.dependencies import PaginationDep
from src.schemas.hotels import Hotel, HotelPatch

from src.database import async_session_maker, engine

from src.models.hotels import HotelsOrm


router = APIRouter(prefix="/hotels")


@router.get("")
async def get_hotels(
    pagination: PaginationDep,
    title: str | None = Query(None, description="Название отеля"),
    location: str | None = Query(None, description="Расположение отеля"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:

        query = select(HotelsOrm)
        if title:
            query = query.filter(HotelsOrm.title.like(f"%{title}%"))
        if location:
            query = query.filter(HotelsOrm.locations.like(f"%{location}%"))
        query = query.limit(per_page).offset(per_page * (pagination.page - 1))  # type: ignore

        print(query.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await session.execute(query)
        hotels = result.scalars().all()
        return hotels


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int):
    # global hotels
    # hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


@router.post("")
async def create_hotel(
    # title: str = Body(embed=True),
    # name: str = Body(embed=True),
    hotel_data: Hotel = Body(
        openapi_examples={
            "1": {"summary": "Cox", "value": {"title": "Cox", "locations": "cox"}},
            "2": {
                "summary": "Marriott",
                "value": {"title": "Marriott", "locations": "marriott"},
            },
        }
    )
):

    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        print(
            add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True})
        )  # * Вывод сырого SQL запроса
        await session.execute(add_hotel_stmt)
        await session.commit()

    return {"status": "OK"}


@router.put("/{hotel_id}")
async def put_hotel(hotel_id: int, hotel_data: Hotel):
    # if hotel_data.title == "" or hotel_data.name == "":
    #     return {"status": "Input data error"}
    # global hotels
    # for hotel in hotels:
    #     if hotel["id"] == hotel_id:
    #         hotel["title"] = hotel_data.title
    #         hotel["name"] = hotel_data.name
    return {"status": "OK"}


@router.patch(
    "/{hotel_id}",
    summary="Update hotel partially",
    description="<h1>Update hotel partially</h1>",
)
async def patch_hotel(hotel_id: int, hotel_data: HotelPatch):
    # if hotel_data.title == "" and hotel_data.name == "":
    #     return {"status": "Input data error"}
    # for hotel in hotels:
    #     if hotel["id"] == hotel_id:
    #         if hotel_data.title != "" and hotel_data.title is not None:
    #             hotel["title"] = hotel_data.title
    #         if hotel_data.name != "" and hotel_data.name is not None:
    #             hotel["name"] = hotel_data.name
    return {"status": "OK"}
