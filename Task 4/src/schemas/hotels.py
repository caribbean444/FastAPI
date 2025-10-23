from pydantic import BaseModel, Field


class Hotel(BaseModel):
    title: str
    locations: str


class HotelPatch(BaseModel):
    title: str | None = Field(default=None, description="Название отеля")
    locations: str | None = Field(default=None, description="Имя отеля")
