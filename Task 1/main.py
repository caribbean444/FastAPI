from fastapi import Body, FastAPI, Query
import uvicorn

app = FastAPI()

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
]


@app.get("/hotels")
def get_hotels(
    id: int | None = Query(None, description="Id"),
    title: str | None = Query(None, description="Название отеля"),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)

    return hotels_


@app.delete("/holets/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


@app.post("/hotels")
def create_hotel(
        title: str = Body(embed=True),
        name: str = Body(embed=True),
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": title,
        "name": name,
    })
    return {"status": "OK"}


@app.put("/hotels/{hotel_id}")
def put_hotel(
    hotel_id: int,
    title: str = Body(),
    name: str = Body()
):
    if title == "" or name == "":
        return {"status": "Input data error"}
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = title
            hotel["name"] = name
    return {"status": "OK"}


@app.patch("/hotels/{hotel_id}")
def patch_hotel(
    hotel_id: int,
    title: str | None = Body(),
    name: str | None = Body()
):
    if title == "" and name == "":
        return {"status": "Input data error"}
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if title != "":
                hotel["title"] = title
            if name != "":
                hotel["name"] = name
    return {"status": "OK"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
