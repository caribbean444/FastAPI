from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey

from src.database import BaseORM


class RoomsOrm(BaseORM):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    title: Mapped[int]
    description: Mapped[str | None]
    price: Mapped[int]
    quantity: Mapped[int]
