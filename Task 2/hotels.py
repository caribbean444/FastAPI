from fastapi import Body, APIRouter, Query
from pydantic import BaseModel, Field

from schemas.hotels import Hotel, HotelPatch


router = APIRouter(prefix="/hotels")

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]



@router.get("")
async def get_hotels(
    id: int | None = Query(None, description="Id"),
    title: str | None = Query(None, description="Название отеля"),
    page: int | None = Query(1, description="Номер страницы"),
    per_page: int | None = Query(3, description="Количество отелей на странице")
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    print(page, per_page)
    if page > 0 and per_page > 0 : # type: ignore
        start = (page - 1) * per_page # type: ignore
        end = start + per_page # type: ignore
        return hotels_[start:end]
    else:
        return {"status": "Invalid page or per_page"}
    return hotels_


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


@router.post("")
async def create_hotel(
        # title: str = Body(embed=True),
        # name: str = Body(embed=True),
        hotel_data: Hotel = Body(openapi_examples=
        {
            "1": {"summary": "Cox", "value": {"title": "Cox", "name": "cox"}},
            "2": {"summary": "Marriott", "value": {"title": "Marriott", "name": "marriott"}},
        })
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": hotel_data.title,
        "name": hotel_data.name,
    })
    return {"status": "OK"}


@router.put("/{hotel_id}")
async def put_hotel(
    hotel_id: int,
    hotel_data: Hotel
):
    if hotel_data.title == "" or hotel_data.name == "":
        return {"status": "Input data error"}
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = hotel_data.title
            hotel["name"] = hotel_data.name
    return {"status": "OK"}


@router.patch("/{hotel_id}", summary="Update hotel partially", description="<h1>Update hotel partially</h1>")
async def patch_hotel(
    hotel_id: int,
    hotel_data: HotelPatch
):
    if hotel_data.title == "" and hotel_data.name == "":
        return {"status": "Input data error"}
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if hotel_data.title != "" and hotel_data.title is not None:
                hotel["title"] = hotel_data.title
            if hotel_data.name != "" and hotel_data.name is not None:
                hotel["name"] = hotel_data.name
    return {"status": "OK"}
