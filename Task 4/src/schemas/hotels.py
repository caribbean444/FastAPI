from pydantic import BaseModel, Field

class Hotel(BaseModel):
    title: str
    name: str

class HotelPatch(BaseModel):
    title: str | None = Field(default=None, description="Название отеля")
    name: str | None = Field(default=None, description="Имя отеля")